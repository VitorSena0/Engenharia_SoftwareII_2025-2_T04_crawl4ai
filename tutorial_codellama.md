# Guia: rodar “codellama-issues-e-pasta-principal.ipynb” no Kaggle Notebooks

Notebook (permalink): [codellama-issues-e-pasta-principal.ipynb](https://github.com/VitorSena0/Engenharia_SoftwareII_2025-2_T02_crawl4ai/blob/b7ead6c8bf48b9c8eace4126c6e0dc910acb3b5e/codellama-issues-e-pasta-principal.ipynb)

---

## 1) Criar o Notebook no Kaggle

1. Acesse: https://www.kaggle.com/code
2. Clique em “Create Notebook”.
3. Nas “Settings” (ícone de engrenagem, canto direito):
   - Accelerator: CPU (ou GPU se precisar, veja observações em Modelos).
   - Internet: ON (necessário para `pip install` e baixar modelos).
4. Importe o arquivo do GitHub:
   - Baixe o `.ipynb` do link acima e, no Kaggle, use File > Upload Notebook para enviar; ou
   - Copie o conteúdo e crie um novo notebook colando as células (menos recomendado).

---

## 2) Instalar dependências (primeira célula)

Execute uma célula no topo com as instalações. Ajuste conforme as importações do seu notebook (instale só o necessário).

```python
%pip -q install -U pip

# Núcleo LLM/HF (opção recomendada via API do HF; ver seção 4)
%pip -q install "huggingface_hub>=0.23" "transformers>=4.43" accelerate

# Integrações comuns
%pip -q install python-dotenv PyGithub

# Se o projeto usa crawl4ai
%pip -q install crawl4ai

# Torch (opcional): instale somente se for fazer inferência local
# CPU:
# %pip -q install "torch==2.3.1" --index-url https://download.pytorch.org/whl/cpu
# GPU (se o ambiente Kaggle já trouxer torch com CUDA, muitas vezes NÃO precisa instalar)
```

---

## 3) Segredos (tokens) no Kaggle

Se o notebook cria issues no GitHub e/ou usa modelos do Hugging Face, você precisa de tokens:

- Hugging Face: `HUGGINGFACEHUB_API_TOKEN`
- GitHub: `GITHUB_TOKEN` (com escopo `repo` para criar issues)

Como adicionar:
1. No notebook do Kaggle, clique em “Add-ons” > “Secrets”.
2. Adicione chaves com exatamente estes nomes:
   - `HUGGINGFACEHUB_API_TOKEN`
   - `GITHUB_TOKEN`

Como ler no código (recomendado no início do notebook):

```python
import os
from kaggle_secrets import UserSecretsClient

user_secrets = UserSecretsClient()
os.environ["HUGGINGFACEHUB_API_TOKEN"] = user_secrets.get_secret("HUGGINGFACEHUB_API_TOKEN") or ""
os.environ["GITHUB_TOKEN"] = user_secrets.get_secret("GITHUB_TOKEN") or ""


```

---

## 4) Sobre modelos (Code Llama e alternativas)

Rodar Code Llama localmente no Kaggle pode exigir GPU e memória considerável (modelos 7B+ são pesados).
Para simplificar e evitar problemas de memória:

- Recomendado: use a Inference API do Hugging Face (chamadas HTTP), que funciona bem no Kaggle:
  ```python
  from huggingface_hub import InferenceClient
  import os

  client = InferenceClient(
      model="codellama/CodeLlama-7b-Instruct-hf",
      token=os.environ["HUGGINGFACEHUB_API_TOKEN"]
  )

  prompt = "Liste 5 tarefas (issues) para organizar a pasta principal de um projeto Python."
  text = client.text_generation(prompt, max_new_tokens=200, temperature=0.3)
  print(text)
  ```

- Alternativa (inferência local com Transformers): use modelos menores ou com quantização; pode exigir GPU:
  ```python
  from transformers import pipeline

  # Ajuste o modelo para algo menor/compatível com o acelerador do Kaggle
  model_id = "codellama/CodeLlama-7b-Instruct-hf"  # Troque se necessário
  generator = pipeline(
      "text-generation",
      model=model_id,
      device_map="auto",
      torch_dtype="auto"
  )
  out = generator("Gere 3 issues com título e descrição.", max_new_tokens=200)
  print(out[0]["generated_text"])
  ```
---

## 5) Pastas e arquivos no Kaggle

- Diretório de trabalho: `/kaggle/working`
- Datasets (somente leitura): `/kaggle/input/...`

Salvar saídas:
```python
import os, json

os.makedirs("outputs", exist_ok=True)
with open("outputs/issues_propostas.json", "w", encoding="utf-8") as f:
    json.dump({"exemplo": ["issue 1", "issue 2"]}, f, ensure_ascii=False, indent=2)

print("Arquivos em outputs/:", os.listdir("outputs"))
```

Para persistir arquivos:
- Clique em “Save Version” (canto superior direito) e selecione “Save & Run All”.
- Tudo em `/kaggle/working` vira “Output” daquela versão do notebook.

---

## 6) Ordem típica das células (adapte ao seu notebook)

1. Instalação de pacotes (`%pip install ...`).
2. Configuração de segredos (Kaggle Secrets).
3. Parâmetros do projeto (ex.: owner/repo, nomes de pastas).
4. Carregamento do modelo (Inference API ou local).
5. Geração de issues/estrutura (lógica principal do notebook).
6. Criação de issues no GitHub (opcional).
7. Salvamento de artefatos em `outputs/`.
8. Verificações finais (links das issues criadas, listagem de arquivos gerados).

---

## 7) Solução rápida de problemas

- “ModuleNotFoundError”: rode a célula de instalação e garanta Internet ON.
- Erro de memória ao carregar o modelo: use Inference API ou um modelo menor; considere GPU.
- 403/401 na Inference API: confira `HUGGINGFACEHUB_API_TOKEN` em Add-ons > Secrets.
- 404/Permission no GitHub: verifique `GITHUB_TOKEN` (escopo repo) e se você tem acesso ao repositório.
- Saídas não persistem: clique em “Save Version” após gerar os arquivos.

---
