import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Dashboard HRV", layout="wide", page_icon=":bar_chart:")

# CSS customizado para visual limpo com fundo branco e fontes modernas
st.markdown("""
    <style>
        body {
            background-color: #ffffff;
            color: #333;
            font-family: 'Segoe UI', sans-serif;
        }
        .main > div:first-child {
            background-color: #ffffff;
            padding: 1rem 2rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.title("Dashboard HRV - Comparativo: Dezembro vs. Janeiro")

# =========================
# Dados de Comparação
# =========================

# Valores dos indicadores monetários e financeiros
data_comparisons = {
    "Receita": {"Dezembro": 15191 + 2706, "Janeiro": 15191},
    "Custo Fixo": {"Dezembro": 3850.34 + 557.55, "Janeiro": 3850.34},
    "Custos Operacionais": {"Dezembro": 1696.83 + 1521.11, "Janeiro": 1696.83},
    "Custo por Cliente": {"Dezembro": 193.99 + 76.99, "Janeiro": 193.99},
    "Custo Total": {"Dezembro": 5547.17 + 2078.66, "Janeiro": 5547.17},
    "Taxa Asaas": {"Dezembro": 154.66 - 15.73, "Janeiro": 154.66},
    "Juros Recebido": {"Dezembro": 300.00 - 204.00, "Janeiro": 300.00}
}

# Dados percentuais para % Custo Asaas na Receita
data_comparisons_pct = {
    "% Custo Asaas": {"Dezembro": 1.04 + 0.54, "Janeiro": 1.04}
}

# Combina os dados em um único dicionário
data_metrics = dict(data_comparisons)
data_metrics["% Custo Asaas"] = data_comparisons_pct["% Custo Asaas"]

# =========================
# Definição dos KPIs do tipo custo
# (Para estes, a redução é positiva → delta_color="inverse")
# =========================
cost_kpis = ["Custo Fixo", "Custos Operacionais", "Custo por Cliente", "Custo Total", "Taxa Asaas", "% Custo Asaas"]

# =========================
# Exibição dos Cartões de Métricas
# =========================

st.markdown("### Principais Indicadores")

# Determina o número de colunas para distribuir os cartões
num_kpis = len(data_metrics)
num_cols = 4  # por exemplo, 4 cartões por linha
cols = st.columns(num_cols)

# Loop para exibir cada métrica
i = 0
for kpi, values in data_metrics.items():
    dec_value = values["Dezembro"]
    jan_value = values["Janeiro"]
    # Calcula a variação: (Janeiro - Dezembro)
    delta = jan_value - dec_value

    # Formata os valores conforme o tipo de dado (monetário ou percentual)
    if kpi == "% Custo Asaas":
        value_str = f"{jan_value:.2f}%"
        delta_str = f"{abs(delta):.2f}%"
    else:
        value_str = f"R$ {jan_value:,.2f}"
        delta_str = f"R$ {abs(delta):,.2f}"
    
    # Define a lógica de cores:
    # Para custos (incluindo Taxa Asaas e % Custo Asaas): redução (delta negativo) é bom → delta_color="inverse"
    # Para Receita e Juros Recebido: aumento (delta positivo) é bom → delta_color="normal"
    if kpi in cost_kpis:
        delta_color = "inverse"  # significa: se delta é negativo (redução), aparece em verde
    else:
        delta_color = "normal"   # se delta é positivo (aumento), aparece em verde

    # Monta a string do delta com sinal
    sign = "-" if delta < 0 else "+"
    delta_display = f"{sign}{delta_str}"
    
    # Exibe a métrica no cartão
    cols[i].metric(label=kpi, value=value_str, delta=delta_display, delta_color=delta_color)
    
    i = (i + 1) % num_cols

# (Não há mais gráficos nem tabela, conforme solicitado)
