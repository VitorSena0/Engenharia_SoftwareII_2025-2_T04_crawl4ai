# Identificação de Padrões Arquiteturais — `crawl4ai`

> Repositório com os artefatos, scripts e instruções para reproduzir a Atividade 1 da disciplina Engenharia de Software II (2025.2): identificação e comparação de padrões arquiteturais no projeto `crawl4ai` com o apoio de modelos de linguagem.

---

## Sumário
- [Visão Geral](#visão-geral)
- [Artefatos incluídos](#artefatos-incluídos)
- [Modelos utilizados (Hugging Face)](#modelos-utilizados-hugging-face)
- [Metodologia e scripts principais](#metodologia-e-scripts-principais)
- [Tutoriais por LLM](#tutoriais-por-llm)
  - [CodeLlama 7B](#codellama-7b)
  - [Qwen/Qwen2.5-Coder-7B-Instruct](#qwenqwen25-coder-7b-instruct)
  - [CodeBERT](#codebert)
  - [Espaço para outras LLMs](#espaço-para-outras-llms)
- [Principais achados (resumo)](#principais-achados-resumo)
- [Limitações e cuidados](#limitações-e-cuidados)

---

## Visão Geral
Este repositório documenta os procedimentos e contém os artefatos usados para identificar padrões arquiteturais no projeto alvo `crawl4ai`. A análise foi conduzida com três estratégias principais:

1. **Análise automática de issues** (pipeline que resume e classifica issues do GitHub em temas arquiteturais);
2. **Análise do código-fonte por modelos de linguagem** (extração de "esqueleto" do código + perguntas factuais ao modelo);
3. **Análise manual** (leitura crítica do código, README e histórico de commits).

O objetivo é correlacionar as evidências (issues, código, documentação) e produzir um laudo que relacione trechos do código a padrões de arquitetura e padrões de projeto.

---

## Artefatos incluídos
- `src/` - scripts reutilizáveis (ex.: code_to_mermaid.py).
- `tutorial/` — Contém o relatório/tutorial do projeto.
- `docs/` — Documentos e materiais de apoio (PDFs, tutoriais, respostas em MD).
- `notebooks/` — Notebooks Jupyter com análises, experimentos e provas de conceito.
- `read.me` — Explicação do projeto


---

## Modelos utilizados (Hugging Face)
No estudo foram testados e comparados modelos com diferentes perfis (tamanho, foco em código e instrução):

- `MiniMaxAI/MiniMax-M2` — modelo pequeno/rápido para análise textual (issues).
- `Qwen/Qwen2.5-0.5B` — versão leve do Qwen para síntese e saídas estruturadas (JSON).
- `microsoft/codebert-base` — foco em código, útil para análise estática/trecho de código.
- `codellama/CodeLlama-7b-hf` — modelo maior aplicado à análise de código e interpretação de padrões.

---

## Metodologia e scripts principais
Abaixo estão os passos principais e os scripts propostos para cada etapa. Os scripts são descritos com entrada/saída esperada.

### 1) Coleta de evidências
- **Issues do GitHub**: `scripts/analyze_issues.py`
  - Input: arquivo JSON com issues (`artifacts/issues_raw.json`) ou chamada à API do GitHub.
  - Output: `artifacts/issues_summary/<tema>.json` com resumos por grupo temático.
  - Estratégia prática: "dividir para conquistar" — agrupar títulos e metadados, depois resumir por grupo para evitar estouro de memória.

### 2) Extração do “esqueleto” do código (fatos)
- **AST extraction**: `scripts/extract_skeleton.py`
  - Input: árvore de diretórios do projeto alvo.
  - Output: `artifacts/code_skeleton/<arquivo>.json` com lista de imports, classes, defs e decoradores.
  - Uso: alimentar prompts factuais (ex.: "FATO 3: Há um singleton?") para reduzir alucinações.

### 3) Pipeline LLM (fatos → interpretação)
- **Orquestração**: `scripts/llm_pipeline.py`
  - Passo A: enviar fatos extraídos como perguntas do tipo Sim/Não ao modelo (respostas curtas e previsíveis).
  - Passo B: usar as respostas do Passo A como contexto para pedir ao modelo que liste padrões confirmados.
  - Output: `artifacts/code_facts_reports/<arquivo>_patterns.json`.

### 4) Pós-processamento e consolidação
- `scripts/postprocess_results.py` — gera tabelas comparativas (CSV/Markdown) e o sumário final.

---

## Tutoriais por LLM

### CodeLlama 7B

Esta análise utiliza o notebook `notebooks/codellama-issues-e-pasta-principal.ipynb` para identificar padrões arquiteturais e inspecionar issues do repositório `crawl4ai` usando o modelo **CodeLlama 7B**.

> Tutorial completo: veja [docs/tutorial_codellama.md](docs/tutorial_codellama.md) (quando presente).

#### Infraestrutura Utilizada

Para garantir a reprodutibilidade, a análise foi executada em um ambiente de nuvem específico e contido, com recursos suficientes para replicar o estudo e entender as limitações de hardware:

- **Plataforma de Nuvem:** Kaggle Notebook  
- **Serviço/Recursos:** Instância com acelerador de GPU  
- **GPU:** NVIDIA Tesla T4  
- **VRAM (Memória da GPU):** 16 GB  
- **CPU / RAM:** Configuração padrão do ambiente Kaggle com GPU

A escolha dessa infraestrutura (GPU T4 com 16 GB) foi um fator limitante, exigindo otimizações como **quantização em 4 bits** e **gerenciamento explícito de memória** (detalhados no notebook e no código) para executar o modelo CodeLlama 7B.

#### Reprodutibilidade e Instruções de Execução

O notebook foi projetado para ser totalmente reprodutível:

- Não depende de um `requirements.txt` separado;  
- As dependências são instaladas diretamente na **primeira célula** do notebook;
- Os dados da análise (as **55 issues** utilizadas) estão embutidos no código para garantir que o script sempre gere os mesmos resultados.

##### Como executar

1. **Ambiente**
   - Acesse a plataforma [Kaggle](https://www.kaggle.com/).

2. **Notebook**
   - Crie um novo notebook e carregue o arquivo  
     `notebooks/codellama-issues-e-pasta-principal.ipynb`.
   - Caso tenha clusterizado os arquivos com o CodeBERT-base, carregue o arquivo abaixo ao invés do anterior
     `notebooks/Crawl4ai com Llama (arquivos escolhidos pelo codebert).ipynb`    

3. **Configuração de Hardware**
   - Nas configurações do notebook (painel à direita), defina:
     - `Accelerator`: **GPU (T4 x1)**
     - `Internet`: **ON** (necessário para baixar dependências e o modelo).

4. **Dependências**
   - Execute a **primeira célula de código** do notebook.
   - Ela instalará todas as bibliotecas necessárias (`transformers`, `accelerate`, `bitsandbytes`, `torch`, etc.).

5. **Execução Completa**
   - Execute todas as células do notebook **sequencialmente**.
   - O script irá:
     - Carregar o modelo CodeLlama 7B com quantização apropriada;
     - Analisar os arquivos de código do projeto;
     - Analisar as 55 issues embutidas no próprio notebook;
     - Gerar os resultados: Relatórios de análise descritos no notebook.

---

### Qwen/Qwen2.5-Coder-7B-Instruct

Este tutorial descreve os passos necessários para executar o notebook `notebooks/Analise_Qwen2-5-Coder-7B-Instruct_prompts1e2.ipynb` no Google Colab ou Kaggle, para análise de padrões arquiteturais.

> Tutorial completo: veja [docs/tutorial_Qwen7B_prompt1e2.md](docs/tutorial_Qwen7B_prompt1e2.md).

Pontos principais:

- **Pré-requisitos:** conta no Hugging Face, token com permissão de *Inference*, conta no Colab ou Kaggle.
- **Configuração inicial:** primeira célula clona o repositório `crawl4ai`.
- **Token HF:** configurado como `HF_TOKEN` via *Secrets*:
  - No Colab, usando `google.colab.userdata`;
  - No Kaggle, usando `kaggle_secrets.UserSecretsClient`.
- O notebook oferece duas abordagens:
  - **3.1 Análise de arquivos chave em lote:** gera `respostasP1.md`;
  - **3.2 Análise de arquivos individuais (.py):** gera `respostasP2.md`.

---
### Qwen/Qwen2.5-Coder-0.5B-Instruct
> Tutorial completo: veja [docs/Tutorial_Qwen2.5_0.5B.md](docs/Tutorial_Qwen2.5_0.5B.md).

- Acesse o notebook: [notebooks/AnaliseQwen2_5_0_5B_limpo.ipynb](notebooks/AnaliseQwen2_5_0_5B_limpo.ipynb).
- Envie-o para o Google Colab.
- Execute as células na ordem.

**Notebook automaticamente:**
- Clona o repositório Crawl4AI
- Lê README e árvore de diretórios
- Monta um prompt estruturado
- Carrega o modelo Qwen 0.5B
- Identifica padrões arquiteturais
- Salva arquivos JSON e CSV
- Nenhuma GPU é necessária.
---
### CodeBERT

Este guia mostra como rodar o notebook “Clusterizando arquivos Crawl4ai com o Codebert” no Kaggle Notebooks, usando o modelo `microsoft/codebert-base` para gerar embeddings e clusterizar arquivos `.py`.

> Tutorial completo: veja [docs/tutorial_codebert.md](docs/tutorial_codebert.md).

### Como executar

1.  **Ambiente**
    * Acesse a plataforma [Kaggle](https://www.kaggle.com/).

2.  **Notebook**
    * Crie um novo notebook e carregue o arquivo:
        `notebooks/Clusterizando arquivos Crawl4ai com o Codebert.ipynb`

3.  **Configuração de Hardware**
    * Nas configurações do notebook (painel à direita), defina:
        * `Accelerator`: **CPU** (Suficiente para esta etapa)
        * `Internet`: **ON** (Necessário para baixar dependências, o modelo e clonar o repositório).

4.  **Dependências**
    * Execute a **primeira célula de código** do notebook para instalar as bibliotecas:
        ```python
        !pip install transformers
        !pip install scikit-learn
        !pip install protobuf==3.20.3
        ```

5.  **Execução Completa**
    * Execute todas as células do notebook **sequencialmente**.
    * O script irá:
        1.  Clonar o repositório `crawl4ai` do GitHub.
        2.  Carregar o modelo `microsoft/codebert-base`.
        3.  Ler todos os arquivos `.py` e gerar *embeddings* (vetores) para eles.
        4.  Aplicar K-Means para agrupar os arquivos em 5 clusters.
    * O resultado final será a lista de arquivos de cada cluster, que servirá de entrada para a Fase 2 (CodeLlama).


---
### Qwen/Qwen2.5-Coder-7B-Instruct outra abordagem

Este tutorial descreve os passos necessários para executar o notebook `notebooks/Analise_QWEN2.5-Coder-7B_Crawl4AI.ipynb` no Google Colab, com o objetivo de identificar padrões arquiteturais, camadas e responsabilidades do repositório `crawl4ai`. Toda a análise foi realizada utilizando o modelo **Qwen/Qwen2.5-Coder-7B-Instruct** fornecido via API do Hugging Face, sem necessidade de GPU local.

> Tutorial completo: veja [docs/tutorial_qwen7b.md](docs/tutorial_qwen7b.md)

**Infraestrutura Utilizada**

A análise foi executada em ambiente leve e reprodutível, pois o modelo foi acessado remotamente por API:

- **Plataforma:** Google Colab (versão gratuita)  
- **GPU:** Não necessária  
- **CPU/RAM:** Recursos padrão do Colab (CPU + ~12–15 GB RAM)  
- **Internet:** Obrigatória (para acesso ao Hugging Face)  
- **Dependências externas:** Apenas o token de acesso Hugging Face

Essa abordagem elimina limitações de hardware e permite utilizar modelos de 7B sem instalação local.

**Reprodutibilidade e Instruções Gerais**

O notebook foi construído com foco em reprodutibilidade total:

- Não depende de arquivos locais ou `requirements.txt`  
- Clona automaticamente o repositório `crawl4ai`  
- Instala dependências diretamente na primeira célula  
- As análises Macro e Micro seguem prompts padronizados  
- Gera sempre o mesmo conjunto de artefatos ao final

**Como Executar**

**1. Ambiente**
Acesse o Google Colab:
https://colab.research.google.com/

**2. Notebook**
Carregue o arquivo: [notebooks/AnaliseArquiteturaQwen7b.ipynb](notebooks/AnaliseArquiteturaQwen7b.ipynb).


**3. Autenticação**
Antes de iniciar, gere um token no Hugging Face com permissão de *Inference* e configure-o na primeira célula do notebook.

**4. Configuração**
Execute sequencialmente as células, que realizam:

1. Instalação de dependências  
2. Configuração do cliente Hugging Face  
3. Clonagem do repositório  
4. Coleta de arquivos Python  
5. Análise Macro  
6. Análise Micro  
7. Síntese do relatório final

** Etapas da Análise (realizadas pelo LLM)**

**Análise Macro**
O modelo recebe a lista de arquivos do projeto e identifica:

- Camadas presentes (domínio, infraestrutura, interface etc.)  
- Organização estrutural  
- Módulos essenciais  
- Estilo arquitetural predominante  

Essa etapa produz uma visão global do sistema.

**Análise Micro**
Cada arquivo `.py` é analisado individualmente quanto a:

- Responsabilidade principal  
- Camada à qual pertence  
- Dependências  
- Padrões de projeto utilizados  
- Pontos fortes e oportunidades de melhoria  

As respostas são armazenadas em um arquivo JSON para posterior consulta.

**Síntese Final**
O notebook combina:

- a visão Macro  
- as análises Micro individuais  

E gera automaticamente um **Relatório Técnico de Arquitetura**, contendo:

- arquitetura de alto nível  
- componentes principais  
- padrões arquiteturais observados  
- integrações (browser, rede, Docker, LLMs)  
- pontos fortes e riscos  
- sugestões de melhoria  

Este relatório é salvo como um dos artefatos finais da execução.

---





## Principais achados (resumo)
> Este resumo sintetiza os resultados que estão detalhados no PDF de apresentação.

- **Arquiteturas identificadas:** Microkernel (núcleo + estratégias/plugins), Pipe & Filter (pipeline de processamento de conteúdo), Arquitetura em Camadas (interface → aplicação → domínio → infraestrutura).
- **Padrões de projeto detectados (exemplos):** Cache (`@lru_cache` em `model_loader.py`), Factory Method (funções `load_*`), Semaphore (`asyncio.Semaphore` em `async_dispatcher.py`), Decorator (uso de decoradores em funções utilitárias), entre outros.
- **Evidências relevantes:** Issues específicas (#1527, #1572, #1212, etc.), trechos de `async_webcrawler.py` e `model_loader.py` analisados.

> Para ver as evidências completas consulte o documento `docs/Identificações de Padrões Arquiteturais.pdf` (artefato gerado pelo grupo).

---

## Limitações e cuidados
- **Alucinação de modelos**: grandes LLMs podem contradizer suas próprias respostas se não forem guiados por fatos objetivos; por isso a estratégia "Fato → Interpretação" foi adotada.
- **Viés de amostragem nas issues**: selecionar apenas issues recentes pode mascarar decisões arquiteturais históricas. Agrupar por tema reduz esse viés.
- **Recursos computacionais**: execuções com CodeLlama-7b exigem GPU e memória; caso contrário, usar modelos menores ou dividir contexto.

---
