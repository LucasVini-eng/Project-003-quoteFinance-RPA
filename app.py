import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Quote Analytics ($)",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css(file_path="style.css"):
    """Carrega as regras de estilo CSS a partir de um arquivo externo."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Não foi possível carregar o arquivo CSS ({file_path}): {e}")

load_css("style.css")

@st.cache_data(ttl=60)
def load_sheets_data():
    """Carrega dados da planilha pública do Google Sheets em formato XLSX ou retorna dados mockados de contingência."""
    public_xlsx_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQx6J04PIEGYPmHyx4104LC92FrUsjNLQIy5kwISP53dfIX2qtNTx1KTmGPwZJmZm0a0BWkkAzJZvJ3/pub?output=xlsx"
    
    try:
        # Lê a planilha diretamente do link público via pandas
        df = pd.read_excel(public_xlsx_url)
        return df, None
    except Exception as e:
        # Fallback: Dados simulados se o link não estiver acessível ou sem conexão
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        mock_data = []
        currencies = [
            ("USD", 5.45, 0.05),
            ("EUR", 5.92, 0.04),
            ("CNY", 0.76, 0.01),
            ("BTC", 350000.0, 2500.0),
            ("ETH", 18500.0, 150.0)
        ]
        
        for dt in dates:
            dt_str = dt.strftime("%d/%m/%Y %H:%M:%S")
            for symbol, base_val, std in currencies:
                import random
                val = round(base_val + random.uniform(-std, std), 4 if symbol != "BTC" else 2)
                perc = round(random.uniform(-1.5, 1.8), 2)
                perc_str = f"{perc:+.2f}%".replace(".", ",")
                mock_data.append({
                    "DATA": dt_str,
                    "MOEDA": symbol,
                    "COTAÇÃO": str(val).replace(".", ","),
                    "PERCENTUAL": perc_str
                })
        
        return pd.DataFrame(mock_data), str(e)

def clean_numeric(val_str, symbol=None):
    """Converte valores em texto da planilha para float e ajusta a escala das casas decimais."""
    if val_str is None or pd.isna(val_str):
        return None
    
    if isinstance(val_str, (int, float)):
        val = float(val_str)
    else:
        s = str(val_str).replace("R$", "").replace("$", "").replace(" ", "").strip()
        if not s:
            return None
        
        # Trata delimitadores de milhar e decimal
        if "." in s and "," in s:
            if s.find(".") < s.find(","):
                s = s.replace(".", "").replace(",", ".")
            else:
                s = s.replace(",", "")
        elif "," in s:
            s = s.replace(",", ".")
        elif "." in s:
            parts = s.split(".")
            if len(parts) == 2 and len(parts[1]) == 3 and symbol in ["BTC", "ETH"]:
                s = s.replace(".", "")
                
        try:
            val = float(s)
        except ValueError:
            return None

    if val is None:
        return None

    if symbol in ["USD", "EUR"]:
        if val >= 10000:
            val /= 10000.0  # ex: 51778 -> 5.1778
        elif val >= 100:
            val /= 100.0    # ex: 518 -> 5.18
    elif symbol == "CNY":
        if val >= 1000:
            val /= 10000.0  # ex: 7700 -> 0.77
        elif val >= 10:
            val /= 100.0    # ex: 77 -> 0.77
    elif symbol == "BTC":
        if val < 1000:
            val *= 1000.0   # ex: 329.53 -> 329530.0
    elif symbol == "ETH":
        if val < 500:
            val *= 1000.0   # ex: 9.72 -> 9720.0
    else:
        if 50 < val < 1000:
            val /= 100.0
        elif 10000 <= val < 100000:
            val /= 10000.0

    return val


def clean_percentage(perc_str):
    """Extrai valor numérico percentual em float e corrige escala de inteiros."""
    if perc_str is None or pd.isna(perc_str):
        return 0.0
    
    if isinstance(perc_str, (int, float)):
        val = float(perc_str)
    else:
        s = str(perc_str).replace("%", "").replace("+", "").replace("(", "").replace(")", "").strip()
        if not s:
            return 0.0
        if "." in s and "," in s:
            s = s.replace(".", "").replace(",", ".")
        elif "," in s:
            s = s.replace(",", ".")
        try:
            val = float(s)
        except ValueError:
            return 0.0

    # Corrige se a variação percentual veio multiplicada por 100 (ex: 138% ao invés de 1.38%)
    if abs(val) >= 20.0:
        val /= 100.0

    return val


def parse_date(dt_str):
    """Realiza parse de datas no padrão brasileiro ou objetos datetime do Excel."""
    if dt_str is None or pd.isna(dt_str):
        return None
    if isinstance(dt_str, (datetime, pd.Timestamp)):
        return dt_str
        
    dt_str = str(dt_str).strip()
    formats = ["%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
    for fmt in formats:
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            pass
    return None

df_raw, error_msg = load_sheets_data()

if not df_raw.empty and "DATA" in df_raw.columns:
    df = df_raw.copy()
    df["DATETIME"] = df["DATA"].apply(parse_date)
    df["VALOR_NUM"] = df.apply(lambda row: clean_numeric(row["COTAÇÃO"], row.get("MOEDA")), axis=1)
    df["PERC_NUM"] = df["PERCENTUAL"].apply(clean_percentage)
    df = df.dropna(subset=["DATETIME", "VALOR_NUM"])
    df["DATE_ONLY"] = df["DATETIME"].dt.date
    df = df.sort_values("DATETIME")
else:
    df = pd.DataFrame()

col_header, col_refresh = st.columns([4, 1])
with col_header:
    st.markdown('<div class="main-title">Quote Analytics <span>($)</span></div>', unsafe_allow_html=1)
    st.markdown('<div class="subtitle-text">Monitoramento em tempo real via Google Sheets (Public Link)</div>', unsafe_allow_html=1)

with col_refresh:
    if st.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()

if error_msg:
    st.caption(f"ℹ️ *Exibindo dados de simulação (Não foi possível acessar a URL da planilha: {error_msg})*")

st.markdown("### 📊 Cotações Atuais")

fiat_symbols = ["USD", "EUR", "CNY"]
crypto_symbols = ["BTC", "ETH"]
all_symbols = fiat_symbols + crypto_symbols

metric_cols = st.columns(len(all_symbols))

for idx, symbol in enumerate(all_symbols):
    with metric_cols[idx]:
        sub_df = df[df["MOEDA"] == symbol] if not df.empty else pd.DataFrame()
        if not sub_df.empty:
            latest_row = sub_df.iloc[-1]
            val = latest_row["VALOR_NUM"]
            perc = latest_row["PERC_NUM"]
            
            # Formatação
            if symbol in crypto_symbols:
                val_formatted = f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            else:
                val_formatted = f"R$ {val:.4f}".replace(".", ",")
            
            badge_class = "positive" if perc > 0 else ("negative" if perc < 0 else "neutral")
            perc_prefix = "+" if perc > 0 else ""
            perc_formatted = f"{perc_prefix}{perc:.2f}%".replace(".", ",")
        else:
            val_formatted = "N/A"
            perc_formatted = "0.00%"
            badge_class = "neutral"

        card_html = f"""
        <div class="quote-card">
            <div class="quote-header">
                <span class="quote-symbol">{symbol}/BRL</span>
                <span class="quote-badge {badge_class}">{perc_formatted}</span>
            </div>
            <div class="quote-value">{val_formatted}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=1)

st.markdown("<br>", unsafe_allow_html=1)

st.sidebar.markdown("## ⚙️ Filtros de Análise")

if not df.empty:
    min_date = df["DATE_ONLY"].min()
    max_date = df["DATE_ONLY"].max()
else:
    min_date = datetime.now().date() - timedelta(days=30)
    max_date = datetime.now().date()

# Segmentação de Data
date_range = st.sidebar.date_input(
    "📅 Selecione o Período",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date, format="DD/MM/YYYY"
)

# Aplicar filtro de data
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_d, end_d = date_range
    filtered_df = df[(df["DATE_ONLY"] >= start_d) & (df["DATE_ONLY"] <= end_d)]
else:
    filtered_df = df.copy()

# Filtro de Moedas Tradicionais
selected_fiats = st.sidebar.multiselect(
    "💵 Moedas Tradicionais",
    options=fiat_symbols,
    default=fiat_symbols
)

# Filtro de Criptomoedas
selected_cryptos = st.sidebar.multiselect(
    "🪙 Criptomoedas",
    options=crypto_symbols,
    default=crypto_symbols
)

plotly_theme = dict(
    paper_bgcolor="#13151b",
    plot_bgcolor="#13151b",
    font=dict(color="#f1f5f9", family="Inter, sans-serif"),
    xaxis=dict(
        gridcolor="#1e293b",
        zerolinecolor="#1e293b",
        showline=True,
        linecolor="rgba(184, 110, 40, 0.35)"
    ),
    yaxis=dict(
        gridcolor="#1e293b",
        zerolinecolor="#1e293b",
        showline=True,
        linecolor="rgba(184, 110, 40, 0.35)"
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8")
    ),
    margin=dict(l=40, r=20, t=40, b=40)
)

st.markdown("### 📈 Histórico de Cotações")

tab_fiat, tab_crypto = st.tabs(["💵 Moedas Tradicionais (FIAT)", "🪙 Criptomoedas"])

with tab_fiat:
    fiat_df = filtered_df[filtered_df["MOEDA"].isin(selected_fiats)] if not filtered_df.empty else pd.DataFrame()
    
    if not fiat_df.empty:
        fig_fiat = go.Figure()
        
        fiat_colors = {
            "USD": "#b86e28",
            "EUR": "#38bdf8",
            "CNY": "#a855f7"
        }
        
        for symbol in selected_fiats:
            sub = fiat_df[fiat_df["MOEDA"] == symbol]
            if not sub.empty:
                fig_fiat.add_trace(go.Scatter(
                    x=sub["DATETIME"],
                    y=sub["VALOR_NUM"],
                    mode="lines+markers",
                    name=f"{symbol}/BRL",
                    line=dict(color=fiat_colors.get(symbol, "#b86e28"), width=2.5, shape='spline'),
                    marker=dict(size=5),
                    hovertemplate="%{x|%d/%m %H:%M}<br><b>%{y:.4f} BRL</b><extra></extra>"
                ))
        
        fig_fiat.update_layout(
            title=dict(text="Moedas FIAT (USD, EUR, CNY) vs BRL", font=dict(size=15, color="#b86e28")),
            yaxis_title="Valor (R$)",
            xaxis_title="Data e Hora",
            hovermode="x unified",
            **plotly_theme
        )
        st.plotly_chart(fig_fiat, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para o período e moedas selecionadas.")

with tab_crypto:
    crypto_df = filtered_df[filtered_df["MOEDA"].isin(selected_cryptos)] if not filtered_df.empty else pd.DataFrame()
    
    if not crypto_df.empty:
        fig_crypto = go.Figure()
        
        crypto_colors = {
            "BTC": "#f97316",
            "ETH": "#818cf8"
        }
        
        for symbol in selected_cryptos:
            sub = crypto_df[crypto_df["MOEDA"] == symbol]
            if not sub.empty:
                fig_crypto.add_trace(go.Scatter(
                    x=sub["DATETIME"],
                    y=sub["VALOR_NUM"],
                    mode="lines+markers",
                    name=f"{symbol}/BRL",
                    line=dict(color=crypto_colors.get(symbol, "#f97316"), width=2.5, shape='spline'),
                    marker=dict(size=5),
                    hovertemplate="%{x|%d/%m %H:%M}<br><b>R$ %{y:,.2f}</b><extra></extra>"
                ))
        
        fig_crypto.update_layout(
            title=dict(text="Criptomoedas (BTC, ETH) vs BRL", font=dict(size=15, color="#b86e28")),
            yaxis_title="Valor (R$)",
            xaxis_title="Data e Hora",
            hovermode="x unified",
            **plotly_theme
        )
        st.plotly_chart(fig_crypto, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para o período e criptomoedas selecionadas.")

st.markdown("<br><hr style='border-color: rgba(184, 110, 40, 0.2);'><p style='text-align: center; color: #64748b; font-size: 0.8rem;'>Quote Analytics Dashboard • Desenvolvido com Streamlit</p>", unsafe_allow_html=1)
