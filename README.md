# 📊 Automação de Cotações Financeiras & Pipeline de Dados

### 🔗 Painel Interativo

> **Clique aqui para visualizar o Painel Interativo**

\[<!-- Substitua o # pelo link do seu painel -->](https://project-003-quotefinance-rpa-btxecz6b27dmwymtsnruyd.streamlit.app/)

[📊 Acessar (#)

---

Este projeto consiste em uma **pipeline automatizada de coleta, processamento, armazenamento e visualização de dados do mercado financeiro**.

Utilizando **Python** e **Selenium**, o sistema realiza *web scraping* das cotações das principais moedas e criptomoedas diretamente do **Google Finance**, consolida e trata os dados com **Pandas** e os envia para uma planilha do **Google Sheets** por meio das APIs do **Google Cloud Platform (GCP)**.

Por fim, os dados são consumidos por um painel interativo desenvolvido no **Streamlit**.

---

## Arquitetura da Solução

```text
+-------------------+      Web Scraping       +-------------------+
|                   | --------------------->  |                   |
|  Google Finance   |    Selenium WebDriver   |   Python Script   |
| (Fonte de Dados)  |                         | (Automação / ETL) |
|                   |                         |                   |
+-------------------+                         +-------------------+
                                                       |
                                                       |
                                              Autenticação & Escrita
                                               gspread / OAuth2
                                                       |
                                                       ▼
+-------------------+      Importação de Dados     +-------------------+
|                   | <-------------------------- |                   |
|     Streamlit     |    Conector Google Sheets   |   Google Sheets   |
|  (Dashboard BI)   |                             |    (Database)     |
|                   |                             |                   |
+-------------------+                             +-------------------+
```

---

## 🔄 Fluxo de Dados

### 1. 📥 Coleta — Extract

O **Selenium** executa em modo *headless* (em segundo plano), acessando o **Google Finance** para extrair as cotações atuais e variações percentuais das seguintes moedas e criptomoedas:

- 🇺🇸 USD — Dólar Americano
- 🇪🇺 EUR — Euro
- 🇨🇳 CNY — Yuan Chinês
- ₿ BTC — Bitcoin
- Ξ ETH — Ethereum

### 2. ⚙️ Tratamento — Transform

Os dados coletados passam por um processo de limpeza e padronização utilizando **Pandas**, expressões regulares e métodos de manipulação de strings.

Entre os tratamentos realizados estão:

- Limpeza dos valores coletados;
- Padronização das variações percentuais;
- Ajuste da formatação numérica;
- Organização dos dados em uma estrutura tabular;
- Preparação das informações para armazenamento.

### 3. 📤 Carga — Load

Utilizando a biblioteca **gspread** e credenciais de uma **Service Account** do **Google Cloud Platform**, os dados tratados são enviados dinamicamente para as colunas correspondentes da planilha:

```text
quote_db
```

### 4. 📊 Visualização — Visualize

O **App Web em Streamlit** se conecta à planilha do **Google Sheets** para importar e visualizar os dados coletados.

O dashboard permite acompanhar indicadores e gráficos relacionados às oscilações do mercado financeiro e às variações cambiais.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

| Tecnologia / Biblioteca | Função / Propósito                                              |
| ----------------------- | --------------------------------------------------------------  |
| 🐍 **Python**           | Linguagem principal do projeto                                 |
| 🤖 **Selenium**         | Automação do navegador e *Web Scraping*                        |
| 🐼 **Pandas**           | Manipulação e tratamento dos dados                             |
| 📄 **gspread**          | Integração entre Python e Google Sheets                        |
| 🔐 **oauth2client**     | Gerenciamento de credenciais e autenticação da Service Account |
| ⏱️ **datetime / time**  | Registro temporal e controle de intervalos durante a execução  |
| ☁️ **Google Cloud API** | Integração com Google Sheets API e Google Drive API            |
| 📊 **Streamlit**        | Construção do dashboard e análise dos dados                    |

---
## 🔐 Configuração do Google Cloud Platform (GCP) e Google Sheets

Para vincular o script Python ao Google Sheets, siga os passos abaixo.

### 1. Criar um Projeto no GCP

1. Acesse o **Google Cloud Console**;
2. Crie um novo projeto.

Exemplo:

```text
Finance-Automation
```

---

### 2. Ativar as APIs Necessárias

No painel do GCP:

```text
APIs e Serviços → Biblioteca
```

Procure e ative as seguintes APIs:

- Google Sheets API
- Google Drive API

---

### 3. Criar uma Conta de Serviço — Service Account

Acesse:

```text
APIs e Serviços → Credenciais → Criar Credenciais → Conta de Serviço
```

Em seguida:

1. Defina um nome para a conta;
2. Crie a conta de serviço;
3. Acesse a aba de **Chaves**;
4. Selecione:

```text
Adicionar chave → Criar nova chave → JSON
```

5. Baixe o arquivo JSON gerado;
6. Renomeie o arquivo para:

```text
chave.json
```

> ⚠️ **Importante:** não envie o arquivo `chave.json` para um repositório público.

Adicione-o ao arquivo `.gitignore`:

```gitignore
chave.json
```

---

### 4. Compartilhar a Planilha com a Service Account

1. Abra o arquivo `chave.json`;
2. Localize o campo:

```json
"client_email"
```

3. Copie o e-mail da Service Account;
4. Crie uma planilha no Google Sheets chamada:

```text
quote_db
```

5. Clique em **Compartilhar**;
6. Adicione o e-mail da Service Account como **Editor**.

---

## 🚀 Como Executar o Projeto

### 📋 Pré-requisitos

Antes de executar o projeto, certifique-se de possuir:

- Python 3.8 ou superior;
- Google Chrome instalado;
- Credenciais configuradas no Google Cloud Platform;
- Uma planilha do Google Sheets compartilhada com a Service Account.

---
### 1. Instale as Dependências

```bash
pip install pandas gspread oauth2client selenium
```

---
### 2. Adicione a Credencial do GCP

Insira o arquivo:

```text
chave.json
```

no diretório raiz do projeto.


## 🔮 Melhorias Futuras

Algumas possíveis evoluções para o projeto:

- [ ] Implementar banco de dados para armazenamento histórico;
- [ ] Automatizar a execução utilizando agendamento;
- [ ] Implementar tratamento de erros e sistema de logs;
- [ ] Criar alertas para grandes variações nas cotações;
- [ ] Containerizar a aplicação com Docker;
- [ ] Realizar deploy da automação em ambiente cloud.

---



## 📄 Licença

Este projeto é distribuído sob a licença **MIT**.

Sinta-se à vontade para utilizar, estudar e adaptar o projeto conforme necessário.

---

\<div align="center">

**📊 Desenvolvido com Python, Selenium, Pandas, Google Cloud e Streamlit**

\</div>

