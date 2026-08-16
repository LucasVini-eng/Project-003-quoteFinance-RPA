import time
from datetime import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    WebDriverException,
)

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

try:
    browser = webdriver.Chrome(options=chrome_options)
    browser.get("https://www.google.com/finance/beta")
    time.sleep(3)
except Exception as e:
    print(f"URL INVÁLIDA ou Erro ao iniciar o navegador ⚠️: {e}")
print("> ACESSANDO GOOGLE FINANCE ...")
print("########## INICIANDO COLETA ##########")
def search_finance():
    try:
        search = browser.find_element(
            "xpath", 
            "/html/body/c-wiz[1]/div/div/div[2]/span[1]/div[1]/a"
        )
        search.click()
        time.sleep(3)

        search_select = browser.find_element(
            "xpath",
            "/html/body/c-wiz[5]/div/div[1]/div[2]/div[2]/div[5]/div/div[1]/textarea",
        )
        search_select.click()

    except NoSuchElementException as e:
        print(f"Erro: Elemento não encontrado. Detalhes: {e}")
    except ElementClickInterceptedException:
        print("Erro: Elemento sobreposto, clique interceptado.")
    except WebDriverException as e:
        print(f"Erro geral do Selenium: {e}")
    except Exception as e:
        print(f"Erro inesperado no Search: {e}")


def get_usd_quote():
    print("> Coletando informações do dolar...")
    text_usd = None
    text_usd_perc = None
    try:
        select_usd = browser.find_element(
            "xpath",
            "/html/body/c-wiz[5]/div/div[1]/div[2]/div[2]/div[5]/div/div[1]/textarea",
        )
        select_usd.send_keys("USD/BRL")
        time.sleep(2)

        select_usd_click = browser.find_element(
            "xpath",
            "/html/body/c-wiz[5]/div/div[1]/div[2]/div[2]/div[5]/div/div[2]/div[2]/span/button/div",
        )
        select_usd_click.click()
        time.sleep(4)

        copy_usd = browser.find_element(
            "xpath",
            "/html/body/c-wiz[4]/c-wiz/div/div/div/div[2]/div[2]/div/div/c-wiz/div/div[3]/c-wiz/div/div/div[1]/div/div[2]/div/div[1]/div[1]/span/span",
        )
        text_usd = (
            copy_usd.text.strip() or copy_usd.get_attribute("textContent").strip()
        )

        print("Cotação Atual do USD(R$):", text_usd)

        time.sleep(2)
        copy_usd_perc = browser.find_element(
            "xpath",
            "/html/body/c-wiz[4]/c-wiz/div/div/div/div[2]/div[2]/div/div/c-wiz/div/div[3]/c-wiz/div/div/div[1]/div/div[2]/div/div[1]/div[2]/span/span",
        )
        text_usd_perc = (
            copy_usd_perc.text.strip()
            or copy_usd_perc.get_attribute("textContent").strip()
        )
        print("Percentual atual do USD(%):", text_usd_perc)
        print("##################################")
    except NoSuchElementException as e:
        print(f"Erro: Elemento de cotação não localizado. Detalhes: {e}")
    except Exception as e:
        print(f"Erro inesperado durante a raspagem de USD: {e}")
    finally:
        try:
            browser.get("https://www.google.com/finance/beta")
        except Exception as e:
            print(f"Erro ao redirecionar: {e}")

    return text_usd, text_usd_perc

time.sleep(2)

def get_eur_quote():
    print("> Coletando informações do euro...")
    text_eur = None
    text_eur_perc = None
    try:
        select_eur = browser.find_element(
            "xpath",
            "/html/body/c-wiz[5]/div/div[1]/div[2]/div[2]/div[5]/div/div[1]/textarea",
        )
        select_eur.send_keys("EUR/BRL")
        time.sleep(2)

        select_eur_click = browser.find_element(
            "xpath",
            "/html/body/c-wiz[5]/div/div[1]/div[2]/div[2]/div[5]/div/div[2]/div[2]/span/button/div",
        )
        select_eur_click.click()
        time.sleep(5)

        copy_eur = browser.find_element(
            "xpath",
            "/html/body/c-wiz[4]/c-wiz/div/div/div/div[2]/div[2]/div/div/c-wiz/div/div[3]/c-wiz/div/div/div[1]/div/div[2]/div/div[1]/div[1]/span/span",
        )
        text_eur = (
            copy_eur.text.strip() or copy_eur.get_attribute("textContent").strip()
        )
        print("Cotação do EUR(R$):", text_eur)

        time.sleep(2)
        copy_eur_perc = browser.find_element(
            "xpath",
            "/html/body/c-wiz[4]/c-wiz/div/div/div/div[2]/div[2]/div/div/c-wiz/div/div[3]/c-wiz/div/div/div[1]/div/div[2]/div/div[1]/div[2]/span/span",
        )
        text_eur_perc = (
            copy_eur_perc.text.strip()
            or copy_eur_perc.get_attribute("textContent").strip()
        )
        print("Percentual do EUR(%):", text_eur_perc)
        print("##################################")
    except NoSuchElementException as e:
        print(f"Erro: Elemento de cotação de EUR não localizado. Detalhes: {e}")
    except ElementClickInterceptedException:
        print("Erro: Botão sobreposto na busca de EUR.")
    except WebDriverException as e:
        print(f"Erro geral do Selenium ao buscar EUR: {e}")
    except Exception as e:
        print(f"Erro inesperado durante a raspagem de EUR: {e}")
    finally:
        try:
            browser.get("https://www.google.com/finance/beta")
        except Exception as e:
            print(f"Erro ao redirecionar: {e}")

    return text_eur, text_eur_perc

time.sleep(2)

def get_cny_quote():
    print("> Coletando informações do iene ...")
    text_cny = None
    text_cny_perc = None
    try:
        select_cny = browser.find_element(
            "xpath",
            "/html/body/c-wiz[5]/div/div[1]/div[2]/div[2]/div[5]/div/div[1]/textarea",
        )
        select_cny.send_keys("CNY/BRL")
        time.sleep(2)

        select_cny_click = browser.find_element(
            "xpath",
            "/html/body/c-wiz[5]/div/div[1]/div[2]/div[2]/div[5]/div/div[2]/div[2]/span/button/div",
        )
        select_cny_click.click()
        time.sleep(3)

        copy_cny = browser.find_element(
            "xpath",
            "/html/body/c-wiz[4]/c-wiz/div/div/div/div[2]/div[2]/div/div/c-wiz/div/div[3]/c-wiz/div/div/div[1]/div/div[2]/div/div[1]/div[1]/span/span",
        )
        text_cny = (
            copy_cny.text.strip() or copy_cny.get_attribute("textContent").strip()
        )
        print("Cotação atual do CNY(R$):", text_cny)
        
        time.sleep(2)
        copy_cny_perc = browser.find_element(
            "xpath",
            "/html/body/c-wiz[4]/c-wiz/div/div/div/div[2]/div[2]/div/div/c-wiz/div/div[3]/c-wiz/div/div/div[1]/div/div[2]/div/div[1]/div[2]/span/span",
        )
        text_cny_perc = (
            copy_cny_perc.text.strip()
            or copy_cny_perc.get_attribute("textContent").strip()
        )
        print("Percentual atual do CNY(%):", text_cny_perc)
        print("##################################")
    except NoSuchElementException as e:
        print(f"Erro: Elemento de cotação de CNY não localizado. Detalhes: {e}")
    except ElementClickInterceptedException:
        print("Erro: Botão sobreposto na busca de CNY.")
    except WebDriverException as e:
        print(f"Erro geral do Selenium ao buscar CNY: {e}")
    except Exception as e:
        print(f"Erro inesperado durante a raspagem de CNY: {e}")
    finally:
        try:
            browser.get("https://www.google.com/finance/beta")
        except Exception as e:
            print(f"Erro ao redirecionar: {e}")

    return text_cny, text_cny_perc

time.sleep(2)

def get_btc_quote():
    print("> Coletando informações do bitcoin...")
    text_btc = None
    text_btc_perc = None
    try:
        select_btc = browser.find_element(
            "xpath",
            "/html/body/c-wiz[5]/div/div[1]/div[2]/div[2]/div[5]/div/div[1]/textarea",
        )
        select_btc.send_keys("BTC/BRL")
        time.sleep(2)

        select_btc_click = browser.find_element(
            "xpath",
            "/html/body/c-wiz[5]/div/div[1]/div[2]/div[2]/div[5]/div/div[2]/div[2]/span/button/div",
        )
        select_btc_click.click()
        time.sleep(3)

        copy_btc = browser.find_element(
            "xpath",
            "/html/body/c-wiz[4]/c-wiz/div/div/div/div[2]/div[2]/div/div/c-wiz/div/div[3]/c-wiz/div/div/div[1]/div/div[2]/div/div[1]/div[1]/span/span",
        )
        text_btc = (
            copy_btc.text.strip() or copy_btc.get_attribute("textContent").strip()
        )
        print("Cotação atual do BTC(R$):", text_btc)

        time.sleep(2)
        copy_btc_perc = browser.find_element(
            "xpath",
            "/html/body/c-wiz[4]/c-wiz/div/div/div/div[2]/div[2]/div/div/c-wiz/div/div[3]/c-wiz/div/div/div[1]/div/div[2]/div/div[1]/div[2]/span/span",
        )
        text_btc_perc = (
            copy_btc_perc.text.strip()
            or copy_btc_perc.get_attribute("textContent").strip()
        )
        print("Percentual do BTC(%):", text_btc_perc)
        print("##################################")
    except NoSuchElementException as e:
        print(f"Erro: Elemento de cotação de BTC não localizado. Detalhes: {e}")
    except ElementClickInterceptedException:
        print("Erro: Botão sobreposto na busca de BTC.")
    except WebDriverException as e:
        print(f"Erro geral do Selenium ao buscar BTC: {e}")
    except Exception as e:
        print(f"Erro inesperado durante a raspagem de BTC: {e}")
    finally:
        try:
            browser.get("https://www.google.com/finance/beta")
        except Exception as e:
            print(f"Erro ao redirecionar: {e}")

    return text_btc, text_btc_perc

time.sleep(2)

def get_eth_quote():
    print("> Coletando informações do ether...")
    text_eth = None
    text_eth_perc = None
    try:
        select_eth = browser.find_element(
            "xpath",
            "/html/body/c-wiz[5]/div/div[1]/div[2]/div[2]/div[5]/div/div[1]/textarea",
        )
        select_eth.send_keys("ETH/BRL")
        time.sleep(2)

        select_eth_click = browser.find_element(
            "xpath",
            "/html/body/c-wiz[5]/div/div[1]/div[2]/div[2]/div[5]/div/div[2]/div[2]/span/button/div",
        )
        select_eth_click.click()
        time.sleep(3)

        copy_eth = browser.find_element(
            "xpath",
            "/html/body/c-wiz[4]/c-wiz/div/div/div/div[2]/div[2]/div/div/c-wiz/div/div[3]/c-wiz/div/div/div[1]/div/div[2]/div/div[1]/div[1]/span/span",
        )
        text_eth = (
            copy_eth.text.strip() or copy_eth.get_attribute("textContent").strip()
        )
        print("Cotação do ETH(R$):", text_eth)

        time.sleep(2)
        copy_eth_perc = browser.find_element(
            "xpath",
            "/html/body/c-wiz[4]/c-wiz/div/div/div/div[2]/div[2]/div/div/c-wiz/div/div[3]/c-wiz/div/div/div[1]/div/div[2]/div/div[1]/div[2]/span/span",
        )
        text_eth_perc = (
            copy_eth_perc.text.strip()
            or copy_eth_perc.get_attribute("textContent").strip()
        )
        print("Percentual do ETH(%):", text_eth_perc)

    except NoSuchElementException as e:
        print(f"Erro: Elemento de cotação de ETH não localizado. Detalhes: {e}")
    except ElementClickInterceptedException:
        print("Erro: Botão sobreposto na busca de ETH.")
    except WebDriverException as e:
        print(f"Erro geral do Selenium ao buscar ETH: {e}")
    except Exception as e:
        print(f"Erro inesperado durante a raspagem de ETH: {e}")
    finally:
        try:
            browser.get("https://www.google.com/finance/beta")
        except Exception as e:
            print(f"Erro ao redirecionar: {e}")
    return text_eth, text_eth_perc

def clean_percentage_value(perc_str):
    if not perc_str or pd.isna(perc_str):
        return ""
    s = str(perc_str).replace("%", "").replace("+", "").replace("(", "").replace(")", "").strip()
    if "." in s and "," in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        val = float(s)
        return f"{val:.2f}".replace(".", ",")
    except ValueError:
        return str(perc_str).replace("%", "").replace(".", ",").strip()

def save_quote_by_columns(
    sheet, 
    currency_symbol, 
    value, 
    percentage, 
    expected_headers=None
):

    if expected_headers is None:
        expected_headers = ["DATA", "MOEDA", "COTAÇÃO", "PERCENTUAL"]

    all_values = sheet.get_all_values()
    
    if not all_values:
        sheet.append_row(expected_headers)
        headers = expected_headers
        all_values = [headers]
    else:
        headers = [str(h).strip().upper() for h in all_values[0]]
        
    col_map = {}
    for req_header in expected_headers:
        if req_header in headers:
            col_map[req_header] = headers.index(req_header) + 1
        else:
            new_col_idx = len(headers) + 1
            sheet.update_cell(1, new_col_idx, req_header)
            headers.append(req_header)
            col_map[req_header] = new_col_idx
    next_row = len(all_values) + 1
    current_date = datetime.now().strftime("%d/%m/%Y")
    row_data = {
        "DATA": current_date,
        "MOEDA": currency_symbol,
        "COTAÇÃO": value,
        "PERCENTUAL": clean_percentage_value(percentage)
    }
    for header, col_idx in col_map.items():
        val = row_data.get(header, "")
        sheet.update_cell(next_row, col_idx, val)

    print(f" Dados da moeda '{currency_symbol}'✅")


credencial_json = r"chave.json"
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(credencial_json, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("quote_db")
    sheet = spreadsheet.sheet1
except Exception as e:
    print(f"Erro de autenticação/conexão com Google Sheets: {e}")
    sheet = None


if __name__ == "__main__":
    search_finance()
    value_usd, var_usd = get_usd_quote()
    time.sleep(5)
    
    search_finance()

    value_eur, var_eur = get_eur_quote()
    time.sleep(5)
    search_finance()

    # Coleta cotação do Yuan Chinês
    value_cny, var_cny = get_cny_quote()
    time.sleep(5)
    search_finance()

    # Coleta cotação do Bitcoin
    value_btc, var_btc = get_btc_quote()
    time.sleep(5)
    search_finance()

    # Coleta cotação do Ether
    value_eth, var_eth = get_eth_quote()
    time.sleep(2)

    browser.quit()

    if sheet:
        # Insere dados do Dólar (USD)
        if value_usd:
            save_quote_by_columns(
                sheet=sheet,
                currency_symbol="USD",
                value=value_usd,
                percentage=var_usd
            )
        
        # Insere dados do Euro (EUR)
        if value_eur:
            save_quote_by_columns(
                sheet=sheet,
                currency_symbol="EUR",
                value=value_eur,
                percentage=var_eur
            )
        
        # Insere dados do Yuan Chinês (CNY)
        if value_cny:
            save_quote_by_columns(
                sheet=sheet,
                currency_symbol="CNY",
                value=value_cny,
                percentage=var_cny
            )

        # Insere dados do Bitcoin (BTC)
        if value_btc:
            save_quote_by_columns(
                sheet=sheet,
                currency_symbol="BTC",
                value=value_btc,
                percentage=var_btc
            )

        # Insere dados do Ether (ETH)
        if value_eth:
            save_quote_by_columns(
                sheet=sheet,
                currency_symbol="ETH",
                value=value_eth,
                percentage=var_eth
            )
        
        # Exibe os dados atualizados como DataFrame no terminal
        data_updated = sheet.get_all_records()
        df = pd.DataFrame(data_updated)
        print("\n--- Tabela Atualizada no Google Sheets ---")
        print(df)