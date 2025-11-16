
# Executando o Notebook de Análise de Padrões Arquiteturais com o Modelo Qwen/Qwen2.5-Coder-7B-Instruct no Colab e Kaggle 

Este tutorial descreve os passos necessários para executar o notebook **notebooks/Analise_Qwen2-5-Coder-7B-Instruct_prompts1e2.ipynb** para analisar padrões arquiteturais de software, o notebook foi executado pela equipe utilizando a plataforma do **Google Colab**, porém ele pode ser executado tanto no **Google Colab** como no **Kaggle**.

---

##  Pré-requisitos

- Uma conta no **Hugging Face**.  
- Um **Access Token** do Hugging Face com as permissões da seção *Inference*.
  Você pode criar um na seção **Access Tokens** nas configurações do seu perfil do **Hugging Face**.
- Uma conta no **Google Colab** ou no **Kaggle**.
- Configurações de ambiente utilizadas:
  - Colab:
    - Acelerador de hardware: CPU ou GPUs T4
    - Tipo de ambiente: Python 3
    - Versão de ambiente: Mais recente 
  - Kaggle:
    - Accelerator: GPUs T4
    - Internet: ON


---

##  1. Configuração Inicial (Comum a Colab e Kaggle)

Ambos os ambientes exigem que você execute a primeira célula de código para clonar o repositório.

### 🔽 Clonar o Repositório

Execute a seguinte célula no notebook:

```python
!git clone https://github.com/unclecode/crawl4ai.git
```

Isso fará o download do código-fonte do projeto para o ambiente do notebook.

---

##  2. Configuração do Hugging Face Token

Para usar o modelo **Qwen/Qwen2.5-Coder-7B-Instruct** através do Hugging Face Inference Provider, você deve configurar seu *Access Token* como uma variável de ambiente secreta chamada **HF_TOKEN**.

---

## 🔑 Opção A: Google Colab

1. No painel esquerdo do Colab, clique no ícone de **Chave (Secrets)**.  
2. Clique em **+ Novo Segredo**.  
3. Defina:
   - **Nome:** `HF_TOKEN`
   - **Valor:** seu Hugging Face Access Token  
4. Certifique-se de que **Notebook access** esteja ativado.  
5. Depois, execute a seguinte célula do notebook:

```python
from google.colab import userdata
import os

hf_token = userdata.get('HF_TOKEN')
os.environ['HF_TOKEN'] = hf_token
```

---

## 🔑 Opção B: Kaggle

1. Na barra superior do notebook, clique em **Add-ons**.
2. Clique em **Secrets**  
3. Clique em **Add Secret**.  
4. Defina:
   - **Label:** `HF_TOKEN`
   - **Value:** seu Hugging Face Access Token  
5. Clique em **Save** e verifique se ele aparece na lista.  
6. Execute a seguinte célula do notebook:

```python
import os
from kaggle_secrets import UserSecretsClient

secret_label = "HF_TOKEN"
secret_value = UserSecretsClient().get_secret(secret_label)

os.environ['HF_TOKEN'] = secret_value
```

---

##  3. Execução das Análises

Primeiramente deve-se executar a 4° célula de código do notebook, na qual a variável `system_content` é definida.

Em seguida pode-se avançar para uma das duas abordagens de análise que não devem ser executadas simultaneamente.

O notebook está dividido em duas abordagens principais:

---

### 📂 3.1. Análise de Arquivos Chave em Lote (Seção 1)

Esta seção agrupa os arquivos mais importantes do projeto (como `Dockerfile`, `config.py`, `async_webcrawler.py`) em um único prompt para análise arquitetural.

Passos:

1. **Ler Conteúdo:** execute a 5° célula de código, que carrega o conteúdo dos arquivos-chave na variável `total_content`.
2. **Rodar o Modelo:** execute a 6° célula de código, que usa a API da OpenAI (via Hugging Face Router) para analisar o conteúdo.

A análise será salva em:

```
respostasP1.md
```

---

### 📁 3.2. Análise de Arquivos Individuais (Seção 2)

Esta seção processa todos os arquivos `.py` individualmente.

Passos:

1. **Listar Arquivos:** execute a 7° célula de código, que obtém os caminhos dos arquivos.  
2. **Carregar Conteúdos:** execute a 8° célula de código, que lê os arquivos `.py` e salva no dicionário `file_contents`.  
3. **Rodar o Modelo em Loop:** execute a 9° célula de código, que envia cada arquivo para o modelo.

As respostas individuais serão salvas em:

```
respostasP2.md
```

---

##  4. Armazenamento dos Resultados

Após executar as análises terá os seguintes arquivos:

- **respostasP1.md** → análise de alto nível dos arquivos principais.  
- **respostasP2.md** → análise detalhada arquivo por arquivo.  

Você pode baixar ou visualizar os arquivos diretamente no ambiente.

---

