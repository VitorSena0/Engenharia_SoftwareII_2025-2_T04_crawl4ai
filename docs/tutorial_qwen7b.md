# Tutorial — Análise Arquitetural com Qwen/Qwen2.5-Coder-7B-Instruct  
### Notebook: `Analise_QWEN2.5-Coder-7B_Crawl4AI.ipynb`

Este tutorial descreve, passo a passo, como foi implementado o notebook que realiza a análise arquitetural do repositório `crawl4ai` utilizando o modelo **Qwen/Qwen2.5-Coder-7B-Instruct** via API do Hugging Face.

A ideia geral é:

1. Configurar o ambiente no Google Colab;  
2. Conectar-se ao modelo Qwen 7B via API;  
3. Clonar o repositório `crawl4ai`;  
4. Listar os arquivos `.py` do projeto;  
5. Fazer uma **análise macro** (visão geral da arquitetura);  
6. Fazer uma **análise micro** (arquivo por arquivo);  
7. Gerar um **relatório técnico de arquitetura** com base nas respostas do modelo.

---

## 🧩 1. Infraestrutura Utilizada

A implementação foi feita no **Google Colab**, com:

- Conta Google (para acessar o Colab);  
- Conexão com internet (para acessar GitHub e Hugging Face);  
- **Sem necessidade de GPU**, pois o modelo é acessado via API;  
- Um **token do Hugging Face** com permissão de *Inference*.

> **Como implementar na prática:**  
> 1. Acesse: https://colab.research.google.com/  
> 2. Clique em **"Novo notebook"**.  
> 3. Use as células exatamente na ordem apresentada neste tutorial.

---

## 🛠️ 2. Execução Passo a Passo

Cada subseção abaixo representa uma célula do notebook (ou um pequeno grupo de células).

---

### 📌 2.1 — Instalar Dependências

```python
!pip install -q huggingface_hub
```

**O que isso faz:**  
Instala a biblioteca `huggingface_hub`, que é usada para se conectar à API de inferência do Hugging Face.

**Como implementar no Colab:**  
- Crie uma nova célula no topo do notebook;  
- Cole o comando acima;  
- Execute a célula (Ctrl+Enter ou clicando no botão de "play").

---

### 📌 2.2 — Configurar Token e Cliente Hugging Face

```python
from huggingface_hub import InferenceClient
import os

HF_TOKEN = "hf_SEU_TOKEN_AQUI"

os.environ["HF_TOKEN"] = HF_TOKEN

client = InferenceClient(
    "Qwen/Qwen2.5-Coder-7B-Instruct",
    token=HF_TOKEN,
)
print("Token carregado (prefixo):", HF_TOKEN[:10])
```

**O que isso faz:**

- Importa a classe `InferenceClient` (para mandar requisições ao modelo);  
- Define a variável `HF_TOKEN` com seu token pessoal;  
- Opcionalmente, coloca o token numa variável de ambiente (`os.environ["HF_TOKEN"]`);  
- Cria o `client`, que é o objeto usado para chamar o modelo Qwen 7B;  
- Imprime só o prefixo do token para confirmar que foi carregado.

**Como implementar:**

1. No Hugging Face, vá em **Settings → Access Tokens → New Token** e crie um token com permissão de *Inference*.  
2. Copie o token (começa com `hf_...`).  
3. Substitua `hf_SEU_TOKEN_AQUI` pelo seu token (SEM commitá-lo no GitHub!).  
4. Execute essa célula no Colab.

---

### 📌 2.3 — Função utilitária para conversar com o modelo

```python
def qwen_chat(system_prompt, user_prompt, max_tokens=1024, temperature=0.2):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_prompt},
    ]
    try:
        resp = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-7B-Instruct",
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content
    except Exception as e:
        print("❌ Erro chamando o modelo:", e)
        raise
```

**O que isso faz:**

- Cria uma função que facilita o uso do modelo;  
- Recebe:
  - um `system_prompt` (como o modelo deve se comportar, ex.: “Você é um arquiteto de software sênior”);  
  - um `user_prompt` (a tarefa/questão específica);  
- Monta a lista de mensagens no formato esperado pela API;  
- Chama a API `client.chat.completions.create(...)`;  
- Retorna apenas o texto da resposta (`message.content`).

**Como implementar:**

- Crie uma nova célula logo depois da configuração do cliente HF;  
- Cole esse código;  
- Execute a célula.  
Depois disso, sempre que você quiser falar com o modelo, basta chamar `qwen_chat(...)`.

---

### 📌 2.4 — Clonar o repositório `crawl4ai`

```python
import os, shutil

REPO_URL = "https://github.com/unclecode/crawl4ai.git"
REPO_DIR = "/content/crawl4ai"

os.chdir('/content')

if os.path.exists(REPO_DIR):
    shutil.rmtree(REPO_DIR)

!git clone {REPO_URL} {REPO_DIR}
os.chdir(REPO_DIR)
```

**O que isso faz:**

- Define a URL do repositório (`REPO_URL`) e o diretório de destino (`REPO_DIR`);  
- Garante que estamos em `/content` (diretório padrão do Colab);  
- Se já existir uma pasta `crawl4ai`, apaga ela (`shutil.rmtree`);  
- Usa o comando `git clone` para baixar o repositório;  
- Entra na pasta do projeto com `os.chdir(REPO_DIR)`.

**Como implementar:**

- Crie uma nova célula após a função `qwen_chat`;  
- Cole esse código;  
- Execute.  
Ao final, você terá o código do `crawl4ai` disponível em `/content/crawl4ai`.

---

### 📌 2.5 — Mapear arquivos Python

```python
import os

code_files = []

for root, dirs, files in os.walk("crawl4ai"):
    if "__pycache__" in root:
        continue

    for f in files:
        if f.endswith(".py"):
            code_files.append(os.path.join(root, f))

len(code_files), code_files[:15]
```

**O que isso faz:**

- Usa `os.walk` para percorrer todos os diretórios dentro de `crawl4ai`;  
- Ignora pastas de cache (`__pycache__`);  
- Para cada arquivo que termina com `.py`, adiciona o caminho completo em `code_files`;  
- Ao final, mostra quantos arquivos foram encontrados e uma amostra dos primeiros 15.

**Como implementar:**

- Crie uma nova célula;  
- Cole o código;  
- Execute.  
Guarde a variável `code_files`, pois ela será usada nas análises macro e micro.

---

### 📌 2.6 — Análise Macro da Arquitetura

```python
file_list_preview = "\n".join(code_files[:80])

system_prompt = "Você é um arquiteto de software sênior."
user_prompt = f"""
Estou analisando a arquitetura de software do projeto Crawl4AI (https://github.com/unclecode/crawl4ai).

Abaixo está a lista de arquivos Python principais dentro do pacote `crawl4ai`:

{file_list_preview}

1. Identifique as possíveis CAMADAS ou MÓDULOS (por exemplo: domínio, infraestrutura, interface, API, CLI, etc.).
2. Aponte quais módulos parecem ser o "core" da biblioteca.
3. Sugira qual estilo de arquitetura melhor descreve o projeto (por exemplo: arquitetura em camadas, modular, hexagonal, etc.).
4. Traga hipóteses, deixando claro que são hipóteses baseadas na estrutura de arquivos.

Responda em português, com tópicos bem organizados.
"""

macro_view = qwen_chat(system_prompt, user_prompt, max_tokens=900)
print(macro_view)
```

**O que isso faz:**

- Junta até 80 caminhos de arquivos em uma string (`file_list_preview`);  
- Define que o modelo deve agir como um “arquiteto de software sênior”;  
- Passa a lista de arquivos e pede:
  - identificação de camadas;  
  - módulos core;  
  - estilo arquitetural (camadas, hexagonal, etc.);  
  - hipóteses arquiteturais;  
- Chama `qwen_chat(...)` e salva a resposta em `macro_view`;  
- Imprime o resultado.

**Como implementar:**

- Nova célula;  
- Cole e execute o código;  
- Use o texto impresso como **visão macro** da arquitetura no seu relatório.

---

### 📌 2.7 — Função para análise Micro por arquivo

```python
import pathlib, textwrap

def analisar_arquivo_arquitetura(path):
    caminho = pathlib.Path(path)
    codigo = caminho.read_text(encoding="utf-8", errors="ignore")

    max_chars = 6000
    if len(codigo) > max_chars:
        codigo = codigo[:max_chars]

    user_prompt = f"""
Arquivo: {path}

Código:
```python
{codigo}
```

Com base na minha experiência como arquiteto de software, analise o código acima do ponto de vista de arquitetura de software:
- Qual o papel desse arquivo no projeto (sua responsabilidade primária)?
- A qual camada ou módulo ele pertence (domínio, infraestrutura, interface, etc.)? Explique.
- Quais padrões de projeto podem ser observados (se houver)?
- Há dependências visíveis com outros módulos ou bibliotecas?
- Pontos fortes e possíveis melhorias (arquiteturalmente falando).
"""
    return qwen_chat(
        "Você é um arquiteto de software experiente em projetos Python.",
        user_prompt,
        max_tokens=900
    )
```

**O que isso faz:**

- Lê o conteúdo do arquivo passado em `path`;  
- Limita o tamanho do código para no máximo 6000 caracteres (para não estourar o contexto do modelo);  
- Monta um prompt pedindo uma análise detalhada:
  - responsabilidade do arquivo;  
  - camada;  
  - padrões de projeto;  
  - dependências;  
  - pontos fortes e melhorias;  
- Chama `qwen_chat(...)` com um system prompt específico;  
- Retorna o texto da análise.

**Como implementar:**

- Crie uma nova célula após a análise macro;  
- Cole esse código;  
- Execute.  
Essa função será usada em um loop para analisar todos os arquivos.

---

### 📌 2.8 — Aplicar análise Micro em todos os arquivos

```python
resultados_micro = {}
for f in code_files:
    print(f"Analisando {f}...")
    try:
        resultados_micro[f] = analisar_arquivo_arquitetura(f)
    except Exception as e:
        print(f"❌ Erro ao analisar {f}: {e}")

len(resultados_micro)
```

**O que isso faz:**

- Cria um dicionário `resultados_micro`;  
- Para cada arquivo em `code_files`:
  - imprime qual arquivo está sendo analisado;  
  - chama `analisar_arquivo_arquitetura(f)`;  
  - armazena o resultado textual com a chave igual ao caminho do arquivo;  
- Ao final, mostra quantos arquivos foram analisados com sucesso.

**Como implementar:**

- Crie uma nova célula;  
- Cole esse código;  
- Execute.  
Dependendo da quantidade de arquivos, pode demorar (cada arquivo faz uma chamada à API).

---

### 📌 2.9 — Salvar resultados da análise Micro

```python
import json

with open("/content/analise_micro_crawl4ai.json", "w", encoding="utf-8") as f:
    json.dump(resultados_micro, f, ensure_ascii=False, indent=2)
```

**O que isso faz:**

- Salva o dicionário `resultados_micro` em um arquivo JSON;  
- Cada entrada do JSON contém:
  - o caminho do arquivo Python;  
  - a análise arquitetural textual gerada pelo modelo para aquele arquivo.

**Como implementar:**

- Nova célula;  
- Cole e execute;  
- Depois, você pode baixar o arquivo pelo próprio Colab (barra lateral de arquivos).

---

### 📌 2.10 — Gerar Relatório Final de Arquitetura

```python
micro_resumo = ""
for path, txt in list(resultados_micro.items())[:8]:
    micro_resumo += f"\n### Arquivo: {path}\n{txt}\n"

system_prompt = "Você é um arquiteto de software preparando um relatório técnico para a faculdade."
user_prompt = f"""
Vou te passar:

1) Uma visão macro da estrutura do projeto Crawl4AI.
2) Várias análises micro de arquivos individuais.

Com base nisso, produza um RELATÓRIO DE ARQUITETURA em português contendo:

- Visão geral do projeto (o que ele faz, contexto geral).
- Arquitetura de alto nível (estilo: camadas, modular, etc.).
- Principais componentes/módulos e responsabilidades.
- Como acontece a integração com navegador, rede, LLMs e Docker/API.
- Padrões de projeto importantes detectados (por ex: pipeline, hooks, factories, etc.).
- Pontos fortes da arquitetura.
- Riscos ou possíveis melhorias.

### Visão Macro
{macro_view}

### Visão Micro (por arquivo)
{micro_resumo}
"""

relatorio_final = qwen_chat(system_prompt, user_prompt, max_tokens=1500)
print(relatorio_final)
```

**O que isso faz:**

- Monta um pequeno resumo (`micro_resumo`) com algumas análises micro (para não estourar tokens);  
- Passa para o modelo:
  - o texto da visão macro (`macro_view`);  
  - o resumo das análises micro;  
- Pede explicitamente um **RELATÓRIO DE ARQUITETURA** com:
  - visão geral do projeto;  
  - arquitetura de alto nível;  
  - principais módulos e responsabilidades;  
  - integrações com navegador, rede, LLMs e Docker;  
  - padrões de projeto;  
  - pontos fortes e melhorias;  
- Imprime o relatório final em texto.

**Como implementar:**

- Nova célula;  
- Cole o código;  
- Execute;  
- Copie o texto de `relatorio_final` e salve num `.md` ou `.pdf` para entregar como artefato da disciplina.


---

## ⚠️ 3. Limitações

- O processo depende de um token válido do Hugging Face;  
- É necessário internet para acessar a API;  
- A análise é **estática** (o código não é executado, apenas lido e interpretado como texto);  
- Arquivos muito grandes são truncados para caber no limite de contexto do modelo.

---

## 🎯 4. Conclusão

Este notebook mostra um pipeline completo de **engenharia reversa assistida por IA**, aplicando o modelo **Qwen/Qwen2.5-Coder-7B-Instruct** para extrair:

- camadas arquiteturais;  
- responsabilidades de módulos;  
- padrões de projeto;  
- pontos fortes e oportunidades de melhoria  

no projeto `crawl4ai`.

---
