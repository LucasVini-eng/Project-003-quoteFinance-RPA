# 📊 Automação de Cotações Financeiras & Pipeline de Dados

Este projeto consiste em uma **pipeline automatizada de coleta, processamento, armazenamento e visualização de dados do mercado financeiro**.

Utilizando **Python** e **Selenium**, o sistema realiza *web scraping* das cotações das principais moedas e criptomoedas diretamente do **Google Finance**, consolida e trata os dados com **Pandas** e os envia para uma planilha do **Google Sheets** por meio das APIs do **Google Cloud Platform (GCP)**.

Por fim, os dados são consumidos por um painel interativo desenvolvido no **Streamlit**.

---

## 🏗️ Arquitetura da Solução

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
|     Power BI      |    Conector Google Sheets   |   Google Sheets   |
|  (Dashboard BI)   |                             |    (Database)     |
|                   |                             |                   |
+-------------------+                             +-------------------+
```

---
