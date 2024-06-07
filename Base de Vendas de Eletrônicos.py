#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# In[2]:


# Definir o ID do arquivo e o nome da guia
id_arquivo = "1Jau0eGN1r-iw0m4XXM5NWpBUTHM8T5uPzZZre38sPhk"
nome_arquivo = "0"
arquivo_url = f"https://docs.google.com/spreadsheets/d/{id_arquivo}/export?format=csv&gid={nome_arquivo}"

# Carregar os dados
dados = pd.read_csv(arquivo_url)
dados


# In[ ]:


import gdown
import pandas as pd

# URL do arquivo no Google Drive (substitua 'FILE_ID' pelo ID do seu arquivo)
file_url = 'https://drive.google.com/uc?id=1KJwAnnFekYVCnqAwz8MKmDcLhsQWQQaN'

# Nome do arquivo CSV local onde será salvo
file_name = 'dados.csv'

# Baixar o arquivo do Google Drive
gdown.download(file_url, file_name, quiet=False)

# Carregar o arquivo CSV para um DataFrame do Pandas
dados = pd.read_csv(file_name)

# Exibir as primeiras linhas para verificar se os dados foram carregados corretamente
print(dados.head())


# In[3]:


# Apagar a coluna 'Unnamed: 9' pois os valores estão vazios.
dados = dados.drop(columns=['Unnamed: 9'])


# In[4]:


# Remover símbolo de moeda e converter para dado tipo float
dados['preco unitário'] = dados['preco unitário'].str.replace('R\$', '', regex=True).str.replace(',', '').astype(float)
# Verificar as primeiras linhas e as estatísticas descritivas dos dados
print(dados.head())
print(dados.describe())


# In[5]:


# Renomear colunas
dados = dados.rename(columns={
    'SKU': 'SKU',
    'produto': 'Produto',
    'qtd vendas': 'Quantidade de Vendas',
    'data venda': 'Data de Venda',
    'loja': 'Loja',
    'preco unitário': 'Preço Unitário',
    'nome': 'Nome',
    'sobrenome': 'Sobrenome',
    'gênero': 'Gênero'
})


# In[6]:


# Número de observações (linhas) no banco de dados
num_observacoes = dados.shape[0]
print(f'Número de observações: {num_observacoes}')
# Número de variáveis (colunas) no banco de dados
num_variaveis = dados.shape[1]
print(f'Número de variáveis: {num_variaveis}')
# Nomes das variáveis (colunas) disponíveis
print('Nomes das variáveis:', dados.columns.tolist())


# In[7]:


dados.info() # Verificar a estrutura do dataframe
print(dados.head()) # Verificar as primeiras linhas dos dados


# In[8]:


# Verificar as estatísticas descritivas dos dados
print(dados.describe())


# In[9]:


# Qual o preço unitário médio?
preco_unitario_medio = dados['Preço Unitário'].mean()
print(f'Preço unitário médio: R${preco_unitario_medio:.2f}')


# In[10]:


# Produto mais vendido (quantidade)
produto_mais_vendido = dados.groupby('Produto')['Quantidade de Vendas'].sum().idxmax()
print(f'Produto mais vendido: {produto_mais_vendido}')


# In[11]:


# Quantidade total de produtos vendidos
quantidade_total_vendida = dados['Quantidade de Vendas'].sum()
print(f'Quantidade total de produtos vendidos: {quantidade_total_vendida}')


# In[12]:


# Total de vendas por loja
vendas_por_loja = dados.groupby('Loja')['Quantidade de Vendas'].sum()
print(vendas_por_loja)


# In[13]:


# Qual loja teve a maior quantidade de vendas?
loja_mais_vendas = dados.groupby('Loja')['Quantidade de Vendas'].sum().idxmax()
print(f'Loja com maior quantidade de vendas: {loja_mais_vendas}')


# In[14]:


# Contagem de compras por gênero
compras_por_genero = dados['Gênero'].value_counts()
print(compras_por_genero)


# In[15]:


registros_vendas = dados.iloc[4:10, :] # Selecionar os registros de vendas do 5º ao 10º
print(registros_vendas) # Imprimir os registros de vendas selecionados


# In[16]:


plt.figure(figsize=(10, 6))
sns.countplot(data=dados, x='Produto', palette='viridis')
plt.title('Vendas por Produto')
plt.xlabel('Produto')
plt.ylabel('Quantidade Vendida')
plt.show()


# In[27]:


# Supondo que seus dados já foram carregados em um DataFrame chamado 'dados'
# Convertendo 'Data de Venda' para datetime no formato MM/DD/YYYY
dados['Data de Venda'] = pd.to_datetime(dados['Data de Venda'], format='%m/%d/%Y')

# Agora, agrupando por mês e somando as vendas
vendas_por_mes = dados.groupby(dados['Data de Venda'].dt.month)['Quantidade de Vendas'].sum()

# Definindo nomes dos meses para melhor visualização
nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

# Plotando o gráfico de barras
plt.figure(figsize=(10, 6))
bars = plt.bar(nomes_meses, vendas_por_mes, color='skyblue')
plt.title('Quantidade de Vendas por Mês')
plt.xlabel('Mês')
plt.ylabel('Quantidade de Vendas')
plt.xticks(rotation=45)
plt.grid(True)

# Adicionando o valor de cada barra na ponta superior
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 1), va='bottom', ha='center', fontsize=8)

plt.show()


# In[29]:


# Gráfico 3: Distribuição de Vendas por Loja
vendas_por_loja = dados.groupby('Loja')['Quantidade de Vendas'].sum()
plt.figure(figsize=(8, 8))
plt.pie(vendas_por_loja, labels=vendas_por_loja.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribuição de Vendas por Loja')
plt.axis('equal')  # Assegura que o gráfico seja desenhado como um círculo
plt.show()


# In[30]:


# Gráfico 4: Distribuição de Vendas por Gênero
# Definir cores para os gêneros
cores = {'M': 'navy', 'F': 'pink'}

# Gráfico de barras com cores personalizadas para cada gênero
plt.figure(figsize=(10, 6))
sns.barplot(x='Gênero', y='Quantidade de Vendas', data=dados, estimator=sum, palette=cores)
plt.title('Distribuição de Vendas por Gênero')
plt.xlabel('Gênero')
plt.ylabel('Quantidade de Vendas')
plt.xticks(rotation=0)
plt.show()


# In[28]:


# Salvando a nova base de dados preparada em um arquivo CSV
dados.to_csv('dados_preparados.csv', index=False)

