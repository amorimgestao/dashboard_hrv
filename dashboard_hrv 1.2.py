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

# =============================================================================
# Dados e Métricas dos Indicadores
# =============================================================================
# Abaixo estão definidos os valores de "Dezembro" (valor base) e "Janeiro" (valor atual) para cada métrica, 
# bem como a variação em valor e (quando aplicável) a variação percentual.
# As regras de cores são:
# - Para "Receita" e "Juros Recebido": aumento (delta positivo) é bom (verde), queda é ruim (vermelho);
# - Para os indicadores de custos (Custo Fixo, Custos Operacionais, Custo por Cliente, Custo Total,
#   Taxa Asaas e % Custo Asaas): redução (delta negativo) é bom (verde, usando delta_color="inverse"), 
#   aumento é ruim (vermelho).
#
# Observação:
# - "Custo por Cliente" foi corrigido para R$ 205,45 em Janeiro. Assim, em Dezembro era de R$ 205,45 + R$ 76,99 = R$ 282,44.
metrics = [
    {
        "name": "Receita",
        "jan": 15191.00,
        "dec": 15191.00 + 2706.00,  # 17897.00
        "delta_val": -2706.00,
        "delta_perc": -13.67,
        "type": "revenue",
        "explanation": ("A Receita representa o total de dinheiro recebido pela empresa a partir das vendas ou serviços prestados. "
                        "Uma queda na receita pode indicar uma diminuição nas vendas ou perda de clientes, o que é negativo.")
    },
    {
        "name": "Custo Fixo",
        "jan": 3850.34,
        "dec": 3850.34 + 557.55,  # 4407.89
        "delta_val": -557.55,
        "delta_perc": -12.64,
        "type": "cost",
        "explanation": ("Custos Fixos são despesas que permanecem constantes independentemente do volume de produção, "
                        "como aluguel e salários fixos. Reduzir esses custos é positivo, pois melhora a margem de lucro.")
    },
    {
        "name": "Custos Operacionais",
        "jan": 1696.83,
        "dec": 1696.83 + 1521.11,  # 3217.94
        "delta_val": -1521.11,
        "delta_perc": -47.27,
        "type": "cost",
        "explanation": ("Custos Operacionais referem-se às despesas diretamente relacionadas à operação do negócio, "
                        "como manutenção e logística. Uma redução nesses custos aumenta a eficiência operacional.")
    },
    {
        "name": "Custo por Cliente",
        "jan": 205.45,  # valor corrigido
        "dec": 205.45 + 76.99,  # 282.44
        "delta_val": -76.99,
        "delta_perc": -27.25,
        "type": "cost",
        "explanation": ("O Custo por Cliente é o valor médio gasto para atender cada cliente. Uma diminuição nesse indicador "
                        "significa que a empresa está se tornando mais eficiente no atendimento.")
    },
    {
        "name": "Custo Total",
        "jan": 5547.17,
        "dec": 5547.17 + 2078.66,  # 7625.83
        "delta_val": -2078.66,
        "delta_perc": -27.25,
        "type": "cost",
        "explanation": ("O Custo Total é a soma de todas as despesas da empresa. Reduzir o custo total é fundamental para aumentar a rentabilidade.")
    },
    {
        "name": "Taxa Asaas",
        "jan": 154.66,
        "dec": 154.66 - 15.73,  # 138.93
        "delta_val": +15.73,
        "delta_perc": +11.32,
        "type": "cost",
        "explanation": ("A Taxa Asaas é o valor cobrado pela plataforma de pagamentos. Embora seja um custo, uma redução nessa taxa é positiva, "
                        "pois impacta menos nos resultados financeiros.")
    },
    {
        "name": "% Custo Asaas",
        "jan": 1.04,  # em %
        "dec": 1.04 + 0.54,  # 1.58%
        "delta_val": -0.54,
        "delta_perc": None,  # Mostramos a variação em pontos percentuais
        "type": "cost",
        "explanation": ("Este indicador mostra o percentual que a Taxa Asaas representa em relação à receita. Uma redução indica "
                        "que o custo da plataforma impacta menos o faturamento.")
    },
    {
        "name": "Juros Recebido",
        "jan": 300.00,
        "dec": 300.00 - 204.00,  # 96.00
        "delta_val": +204.00,
        "delta_perc": +312.5,
        "type": "revenue",
        "explanation": ("Juros Recebidos são os encargos cobrados dos clientes inadimplentes, representando dinheiro extra que entra na empresa. "
                        "Um aumento é positivo, embora possa indicar problemas com inadimplência.")
    }
]

# =============================================================================
# Exibição dos Cards com KPIs e Botão de Informação
# =============================================================================

st.markdown("### Principais Indicadores")

# Define quantos cards por linha (neste exemplo, 4 por linha)
num_cols = 4
cols = st.columns(num_cols)

for i, metric in enumerate(metrics):
    with cols[i % num_cols]:
        # Formata os valores e a variação
        if metric["name"] == "% Custo Asaas":
            value_str = f"{metric['jan']:.2f}%"
            delta_str = f"{abs(metric['delta_val']):.2f}%"
        else:
            value_str = f"R$ {metric['jan']:,.2f}"
            delta_str = f"R$ {abs(metric['delta_val']):,.2f}"
        
        # Se houver variação percentual, formata a string combinada
        if metric["delta_perc"] is not None:
            delta_perc_str = f"{abs(metric['delta_perc']):.2f}%"
            delta_display = f"{'-' if metric['delta_val'] < 0 else '+'}{delta_str} ({'-' if metric['delta_perc'] < 0 else '+'}{delta_perc_str})"
        else:
            delta_display = f"{'-' if metric['delta_val'] < 0 else '+'}{delta_str}"
        
        # Define a lógica de cores:
        # Para "revenue" (Receita e Juros Recebido): aumento (delta positivo) é bom → delta_color="normal"
        # Para "cost" (demais): redução (delta negativo) é bom → delta_color="inverse"
        if metric["type"] == "revenue":
            delta_color = "normal"
        else:
            delta_color = "inverse"
        
        st.metric(label=metric["name"], value=value_str, delta=delta_display, delta_color=delta_color)
        
        # Botão de informação com um ícone "ℹ️"
        with st.expander("ℹ️"):
            st.write(metric["explanation"])

st.markdown("<hr><p style='text-align: center; color: #666;'>Dashboard HRV © 2025</p>", unsafe_allow_html=True)
