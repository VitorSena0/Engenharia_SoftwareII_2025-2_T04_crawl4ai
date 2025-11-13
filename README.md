# Identificação de Padrões Arquiteturais — `crawl4ai`

> Repositório com os artefatos, scripts e instruções para reproduzir a Atividade 1 da disciplina Engenharia de Software II (2025.2): identificação e comparação de padrões arquiteturais no projeto `crawl4ai` usando LLMs e análise manual.

---

## Sumário
- [Visão Geral](#visão-geral)
- [Artefatos incluídos](#artefatos-incluídos)
- [Modelos utilizados (Hugging Face)](#modelos-utilizados-hugging-face)
- [Metodologia e scripts principais](#metodologia-e-scripts-principais)
- [Principais achados (resumo)](#principais-achados-resumo)
- [Limitações e cuidados](#limitações-e-cuidados)

--

## Visão Geral
Este repositório documenta os procedimentos e contém os artefatos usados para identificar padrões arquiteturais no projeto alvo `crawl4ai`. A análise foi conduzida com três estratégias principais:
1. **Análise automática de issues** (pipeline que resume e classifica issues do GitHub em temas arquiteturais);
2. **Análise do código-fonte por modelos de linguagem** (extração de "esqueleto" do código + perguntas factuais ao modelo);
3. **Análise manual** (leitura crítica do código, README e histórico de commits).

O objetivo é correlacionar as evidências (issues, código, documentação) e produzir um laudo que relacione trechos do código a padrões de arquitetura e padrões de projeto.

---

## Artefatos incluídos
- `docs/Identificações de Padrões Arquiteturais.pdf` — relatório final (PDF) com resultados e justificativas.
- `scripts/` — scripts Python para extração de AST, agrupamento de issues, chamadas ao modelo e pós-processamento.
- `notebooks/` — notebooks Jupyter com experimentos exploratórios e visualizações.
- `artifacts/` — saídas geradas (resumos de issues, resultados JSON por arquivo, prompts utilizados, logs).
- `requirements.txt` — dependências Python usadas para reproduzir os experimentos.

> Se algum desses diretórios não existir no repositório atual, usar como _template_ para organizar os artefatos.

---

## Modelos utilizados (Hugging Face)
No estudo foram testados e comparados modelos com diferentes perfis (tamanho, foco em código e instrução):

- `MiniMaxAI/MiniMax-M2` — modelo pequeno/rápido para análise textual (issues).
- `Qwen/Qwen2.5-0.5B` — versão leve do Qwen para síntese e saídas estruturadas (JSON).
- `microsoft/codebert-base` — foco em código, útil para análise estática/trecho de código.
- `codellama/CodeLlama-7b-hf` — modelo maior aplicado à análise de código e interpretação de padrões.

> Links originais e versões estão registrados no PDF de resultados (veja `docs/Identificações de Padrões Arquiteturais.pdf`).

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

## Principais achados (resumo)
> Este resumo sintetiza os resultados que estão detalhados no PDF de apresentação.

- **Arquiteturas identificadas:** Microkernel (núcleo + estratégias/plugins), Pipe & Filter (pipeline de processamento de conteúdo), Arquitetura em Camadas (interface → aplicação → domínio → infraestrutura).
- **Padrões de projeto detectados (exemplos):** Cache (@lru_cache em `model_loader.py`), Factory Method (funções `load_*`), Semaphore (`asyncio.Semaphore` em `async_dispatcher.py`), Decorator (uso parcial em `async_webcrawler.py`), Hook/Plugin (evidências em Issues e módulos `hooks`).
- **Evidências relevantes:** Issues específicas (#1527, #1572, #1212, etc.), trechos do `async_webcrawler.py` e `model_loader.py` analisados.

> Para ver as evidências completas consulte o documento `docs/Identificações de Padrões Arquiteturais.pdf` (artefato gerado pelo grupo).

---

## Limitações e cuidados
- **Alucinação de modelos**: grandes LLMs podem contradizer suas próprias respostas se não forem guiados por fatos objetivos; por isso a estratégia "Fato → Interpretação" foi adotada.
- **Viés de amostragem nas issues**: selecionar apenas issues recentes pode mascarar decisões arquiteturais históricas. Agrupar por tema reduz esse viés.
- **Recursos computacionais**: execuções com CodeLlama-7b exigem GPU e memória; caso contrário, usar modelos menores ou dividir contexto.

---



