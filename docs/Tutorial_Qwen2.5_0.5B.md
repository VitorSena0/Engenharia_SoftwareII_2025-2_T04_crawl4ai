# 📘 Tutorial Completo — Análise Arquitetural com Qwen/Qwen2.5-Coder-0.5B-Instruct

Este tutorial descreve detalhadamente como executar a análise arquitetural do projeto **Crawl4AI** utilizando o modelo **Qwen/Qwen2.5-Coder-0.5B-Instruct** no Google Colab.  
O processo engloba coleta de evidências, execução do modelo, parse das respostas, fallback heurístico e uma etapa experimental de análise do código-fonte via chunking.

---

## 🔧 1. Pré-requisitos

Antes de executar este tutorial, você precisa:

- Conta no **Hugging Face**
- Um **Hugging Face Inference Token**
- Conta no **Google Colab**
- Familiaridade básica com Python e notebooks

O modelo utilizado é:

```
Qwen/Qwen2.5-Coder-0.5B-Instruct
```

Ele roda integralmente em **CPU**, ideal para ambientes sem GPU.

---

## 📥 2. Clonando o repositório do Crawl4AI

```python
from git import Repo
from pathlib import Path
import subprocess

REPO_URL = "https://github.com/unclecode/crawl4ai"
REPO_DIR = Path("/content/crawl4ai_repo")

if REPO_DIR.exists():
    import shutil
    shutil.rmtree(REPO_DIR)

Repo.clone_from(REPO_URL, REPO_DIR)
print("Repositório clonado!")
```

---

## 📑 3. Coleta automática de evidências textuais

```python
def ler(p):
    try:
        return Path(p).read_text(encoding="utf-8", errors="ignore")
    except:
        return ""

readme = ler(REPO_DIR/"README.md")

tree = subprocess.check_output(
    ["bash","-lc", f"cd {REPO_DIR} && find . -maxdepth 3 -type d | sort"]
).decode()

evidencia = f"""
README (trecho):
{readme[:5000]}

--- TREE ---
{tree[:5000]}
"""
print("Evidências coletadas.")
```

---

## 🤖 4. Carregando o modelo Qwen 0.5B no Colab

```python
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

MODEL_ID = "Qwen/Qwen2.5-Coder-0.5B-Instruct"

tok = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
mdl = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, device_map="auto", torch_dtype="auto", trust_remote_code=True
)

gen = pipeline("text-generation", model=mdl, tokenizer=tok)
print("Modelo carregado!")
```

---

## 💬 5. Construindo o prompt de análise arquitetural

```python
messages = [
  {"role": "system",
   "content":
     "Você é um analista de arquitetura. Responda ESTRITAMENTE em JSON..."
  },
  {"role": "user",
   "content":
     "Analise as evidências e identifique PADRÕES ARQUITETURAIS..."
     "\nEVIDÊNCIAS:\n" + evidencia
  }
]

prompt_chat = tok.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
```

---

## 🧠 6. Execução do modelo

```python
out = gen(
    prompt_chat,
    max_new_tokens=380,
    do_sample=False,
    temperature=0.0,
    return_full_text=False
)[0]["generated_text"]

print("Geração bruta:")
print(out[:800])
```

---

## 📦 7. Parse do JSON + fallback heurístico

```python
def extrair_bloco_json(texto):
    ini = texto.find("{")
    fim = texto.rfind("}")
    return texto[ini:fim+1] if ini != -1 and fim != -1 else texto
```

Fallback usado:

```python
if "webhook" in ev_txt:
    pats.append({"name":"Event-Driven","confidence":0.75,"evidence":"Menções a eventos/webhooks."})
```

---

## 💾 8. Salvando os arquivos de saída

Os arquivos gerados:

```
patterns_qwen.json
patterns_qwen_summary.csv
```

---

## 🧩 9. Fase experimental — análise de código-fonte (chunking)

O modelo não conseguiu interpretar corretamente os arquivos `.py` devido às limitações de tamanho.  
Mesmo assim, o método de chunking funcionou tecnicamente.

---

## 📊 10. Padrões identificados

| Padrão Arquitetural      | Confiança | Evidência |
|-------------------------|-----------|-----------|
| Event-Driven            | 0.75–0.90 | Webhooks, eventos |
| Plugin/Hook             | 0.72–0.80 | Sistema de extensões |
| Cloud-Native            | ~0.70     | Docker/Compose |

---

## 🎯 11. Conclusão

O modelo Qwen 0.5B funciona bem para análises de documentação,  
mas é insuficiente para análise aprofundada de código-fonte.

---

## 👤 12. Contribuição Individual

- Execução da análise arquitetural  
- Implementação do fallback  
- Análise experimental do código  
- Organização da metodologia e resultados  

---
