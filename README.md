# 🤖 Scripts de Automação

Coleção de scripts Python desenvolvidos para automatizar tarefas rotineiras e processos de análise de dados.

## 📋 Índice

- [Sobre](#sobre)
- [Scripts Disponíveis](#scripts-disponíveis)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)

## 🎯 Sobre

Este repositório tem como objetivo centralizar e manter scripts de automação que facilitam o dia a dia, desde análise de dados até organização de arquivos.

## 🛠️ Scripts Disponíveis

### 1. Analisador de Frequência de Palavras
**Arquivo:** `analisador_frequencia_de_palavras.py`

Analisa a frequência de palavras em um texto, identificando as palavras mais comuns.

**Funcionalidades:**
- Remove pontuação e converte texto para minúsculas
- Conta a frequência de cada palavra
- Ordena e exibe as palavras mais frequentes
- Mostra o total de palavras únicas

**Uso típico:** Análise de textos, documentos e conteúdo textual.

### 2. Contador de Provedores de E-mail
**Arquivo:** `contador_provedoresSplit.py`

Analisa uma lista de e-mails e identifica os provedores mais utilizados.

**Funcionalidades:**
- Extrai o provedor de cada endereço de e-mail
- Conta a frequência de cada provedor
- Exibe os 5 provedores mais comuns

**Uso típico:** Análise de listas de e-mails, mapeamento de provedores em bases de dados.

### 3. Fechamento Mensal de Estoque
**Arquivo:** `fechamento_mensal.py`

Processa planilhas de estoque em formato Excel, aplicando filtros e categorizações específicas.

**Funcionalidades:**
- Lê planilhas Excel (.xlsx) de estoque
- Filtra armazéns específicos conforme configuração
- Calcula valor total de estoque por armazém
- Categoriza materiais por tipo (Cal, Ferroligas, Refratários, EPIs, etc.)
- Exibe valores formatados em reais (R$)

**Uso típico:** Relatórios mensais de fechamento de estoque, análise financeira de inventário.

**Configuração necessária:**
- Arquivo de entrada: `analise_estoque.xlsx`
- Colunas esperadas: 'Local', '(D)Custo Total', 'Grupo'

### 4. Organizador de Arquivos
**Arquivo:** `organizador_arquivos.py`

Organiza arquivos em pastas por tipo/extensão automaticamente.

**Funcionalidades:**
- Interface gráfica para seleção de pasta
- Organiza arquivos por extensão em subpastas:
  - **imagens**: .png, .jpg, .jpeg
  - **planilhas**: .xlsx
  - **pdfs**: .pdf
  - **csv**: .csv
- Cria pastas automaticamente se não existirem
- Move arquivos para suas respectivas categorias

**Uso típico:** Organização de downloads, limpeza de diretórios desorganizados.

## 📦 Pré-requisitos

- Python 3.7 ou superior
- Bibliotecas listadas em `requirements.txt`

## 🔧 Instalação

1. Clone este repositório ou faça o download dos arquivos

2. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

As principais bibliotecas utilizadas são:
- `pandas` - Para manipulação de planilhas e dados
- `openpyxl` - Para leitura de arquivos Excel
- `tkinter` - Interface gráfica (geralmente já incluído no Python)

## 💻 Como Usar

Cada script pode ser executado individualmente:

```bash
# Analisador de frequência de palavras
python analisador_frequencia_de_palavras.py

# Contador de provedores
python contador_provedoresSplit.py

# Fechamento mensal (certifique-se de ter a planilha analise_estoque.xlsx)
python fechamento_mensal.py

# Organizador de arquivos (abrirá uma janela para selecionar a pasta)
python organizador_arquivos.py
```

## 📝 Notas

- Para o script de fechamento mensal, ajuste o nome do arquivo e as colunas conforme sua planilha
- O organizador de arquivos move os arquivos permanentemente, faça backup se necessário
- Alguns scripts contêm dados de exemplo para demonstração

---

**Desenvolvido por:** Diego Bernardes - DBSolutions Lab 
**Última atualização:** Fevereiro 2026
