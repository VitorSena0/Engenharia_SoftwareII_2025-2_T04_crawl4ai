# Guia: rodar “Clusterizando arquivos Crawl4ai com o Codebert” no Kaggle Notebooks

Notebook (permalink): [Clusterizando arquivos Crawl4ai com o Codebert.ipynb](https://github.com/VitorSena0/Engenharia_SoftwareII_2025-2_T02_crawl4ai/blob/main/Clusterizando%20arquivos%20Crawl4ai%20com%20o%20Codebert.ipynb)

-----

## 1\) Criar o Notebook no Kaggle

1.  Acesse: [https://www.kaggle.com/code](https://www.kaggle.com/code)
2.  Clique em **“Create Notebook”**.
3.  Nas **“Settings”** (ícone de engrenagem, canto direito):
      * **Accelerator:** CPU (geralmente suficiente para este notebook, pois o CodeBERT é leve) ou GPU (se disponível, acelera a inferência).
      * **Internet:** ON (necessário para instalar pacotes, clonar o repositório e baixar o modelo CodeBERT).
4.  Importe o arquivo do GitHub:
      * Baixe o `.ipynb` do link acima e, no Kaggle, use **File \> Upload Notebook** para enviar; ou
      * Copie o conteúdo das células do seu notebook local e cole em um novo notebook no Kaggle.

-----

## 2\) Instalar dependências (primeira célula)

Execute a primeira célula para instalar as bibliotecas necessárias. Este passo é crucial para configurar o ambiente.

```python
# Instalar as bibliotecas necessárias
!pip install transformers
!pip install scikit-learn

# Instalação específica de versão do protobuf para evitar conflitos comuns no Kaggle
!pip install protobuf==3.20.3
```

> **Nota:** A instalação do `protobuf==3.20.3` corrige um conflito de versão frequente entre o TensorFlow (pré-instalado no Kaggle) e a biblioteca `transformers`.

-----

## 3\) Preparar o Repositório Alvo (Clonar)

Como o notebook analisa o código do repositório `crawl4ai`, você precisa cloná-lo para o ambiente do Kaggle.

1.  Adicione uma célula para limpar qualquer versão antiga e clonar o repositório novamente. Isso garante que você esteja analisando a versão mais recente ou a desejada.

<!-- end list -->

```python
# REMOVER o diretório antigo, se existir, para garantir um clone limpo
!rm -rf crawl4ai

# Clonar o repositório
!git clone https://github.com/unclecode/crawl4ai.git
```

2.  (Opcional) Você pode listar os arquivos para verificar se o clone funcionou corretamente:
    ```python
    !ls -R crawl4ai
    ```

-----

## 4\) Carregar o Modelo CodeBERT

Nesta etapa, o notebook carrega o modelo `microsoft/codebert-base` da Hugging Face. Este modelo será usado para gerar os *embeddings* (representações vetoriais) dos arquivos de código.

  * Não é necessário configurar tokens de API (Hugging Face) para este modelo, pois ele é público.
  * Certifique-se de que a Internet esteja ligada nas configurações do notebook.

<!-- end list -->

```python
import torch
from transformers import AutoTokenizer, AutoModel
import os
import numpy as np

model_name = "microsoft/codebert-base"

print("Carregando tokenizer e modelo...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
model.eval() # Coloca o modelo em modo de avaliação (inferência)
print("Sucesso!")
```

-----

## 5\) Gerar Embeddings e Clusterizar

O núcleo do notebook envolve duas etapas principais:

1.  **Gerar Embeddings:** O código percorre todos os arquivos `.py` do repositório clonado, lê o conteúdo e usa o CodeBERT para criar um vetor numérico que representa o significado semântico do código.

      * *Dica:* O código já trata arquivos vazios e trunca arquivos muito longos para caber no limite do modelo (512 tokens).

2.  **Clusterização (K-Means):** Com os vetores prontos, o algoritmo K-Means agrupa os arquivos em *clusters* (grupos) baseados na similaridade.

      * Você pode ajustar o número de clusters alterando a variável `n_clusters = 5` na célula correspondente.

-----

## 6\) Analisar os Resultados

Após a execução, o notebook exibe duas saídas principais para análise:

1.  **Lista de Arquivos por Cluster:** Mostra quais arquivos foram agrupados juntos. Isso ajuda a entender a estrutura modular do projeto (ex: arquivos de teste juntos, arquivos de configuração juntos).
2.  **Top Tópicos (Palavras-Chave):** Usa uma técnica simples de contagem de palavras nos nomes dos arquivos para sugerir o "tema" de cada cluster (ex: "crawler", "async", "test").

-----

## 7\) Solução rápida de problemas

  * **Erro "AttributeError: 'MessageFactory' object has no attribute 'GetPrototype'":** Isso geralmente é um problema com a biblioteca `protobuf`. Certifique-se de ter executado a linha `!pip install protobuf==3.20.3` e reiniciado o kernel se necessário.
  * **Erro de Memória (OOM):** Se o repositório for muito grande, o CodeBERT pode consumir muita RAM. No Kaggle, a CPU padrão geralmente aguenta, mas se falhar, tente processar menos arquivos ou usar a GPU.
  * **Diretório não encontrado:** Verifique se o comando `!git clone` foi executado com sucesso e se o caminho `repo_path` no código aponta corretamente para a pasta clonada (ex: `crawl4ai/crawl4ai`).
