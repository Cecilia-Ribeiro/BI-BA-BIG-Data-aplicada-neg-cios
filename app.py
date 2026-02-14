import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Dashboard de Vendas",
    layout="wide"
)

st.title("📊 Dashboard de Análise de Vendas")

# CARREGAR DADOS
@st.cache_data
def carregar_dados():
    df = pd.read_csv("vendas_visualizacao_basica_com_nomes.csv")
    df["data_compra"] = pd.to_datetime(df["data_compra"])
    df["mes"] = df["data_compra"].dt.month
    return df

df = carregar_dados()

# SIDEBAR - FILTROS

st.sidebar.header("🔎 Filtros")

produto = st.sidebar.multiselect(
    "Produto",
    df["produto"].unique(),
    default=df["produto"].unique()
)

cliente = st.sidebar.multiselect(
    "Cliente",
    df["cliente"].unique(),
    default=df["cliente"].unique()
)

periodo = st.sidebar.date_input(
    "Período",
    [df["data_compra"].min(), df["data_compra"].max()]
)

# aplicar filtros
df_filtrado = df[
    (df["produto"].isin(produto)) &
    (df["cliente"].isin(cliente)) &
    (df["data_compra"] >= pd.to_datetime(periodo[0])) &
    (df["data_compra"] <= pd.to_datetime(periodo[1]))
]

# KPIs (MÉTRICAS PRINCIPAIS)

st.subheader("📌 Indicadores principais")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Faturamento Total",
    f"R$ {df_filtrado['faturamento'].sum():,.2f}"
)

col2.metric(
    "🛒 Total de Vendas",
    df_filtrado.shape[0]
)

col3.metric(
    "📦 Quantidade Vendida",
    df_filtrado["quantidade"].sum()
)

col4.metric(
    "💵 Ticket Médio",
    f"R$ {df_filtrado['faturamento'].mean():,.2f}"
)

st.divider()

# GRÁFICOS PRINCIPAIS

col5, col6 = st.columns(2)

# -------- gráfico 1
with col5:
    st.subheader("📦 Faturamento por Produto")

    fig1, ax1 = plt.subplots()
    df_filtrado.groupby("produto")["faturamento"] \
        .sum() \
        .sort_values(ascending=False) \
        .plot(kind="bar", ax=ax1)

    ax1.set_xlabel("Produto")
    ax1.set_ylabel("Faturamento")
    st.pyplot(fig1)

# -------- gráfico 2
with col6:
    st.subheader("💰 Distribuição do Faturamento")

    fig2, ax2 = plt.subplots()
    df_filtrado["faturamento"].hist(ax=ax2)
    ax2.set_xlabel("Faturamento")
    st.pyplot(fig2)

st.divider()

# GRÁFICO TEMPORAL

st.subheader("📈 Evolução do Faturamento ao longo do tempo")

df_tempo = df_filtrado.groupby("data_compra")["faturamento"].sum()

fig3, ax3 = plt.subplots()
df_tempo.plot(ax=ax3)
ax3.set_xlabel("Data")
ax3.set_ylabel("Faturamento")
st.pyplot(fig3)

st.divider()

# INSIGHTS

st.subheader("🧠 Insights Automáticos")

if not df_filtrado.empty:

    produto_top = df_filtrado.groupby("produto")["faturamento"].sum().idxmax()
    cliente_top = df_filtrado.groupby("cliente")["faturamento"].sum().idxmax()
    dia_top = df_filtrado.groupby("data_compra")["faturamento"].sum().idxmax()

    st.write(f"✅ Produto com maior faturamento: **{produto_top}**")
    st.write(f"✅ Cliente que mais comprou: **{cliente_top}**")
    st.write(f"✅ Dia com maior faturamento: **{dia_top.date()}**")

else:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")

st.divider()

# TABELA DE DADOS

st.subheader("📄 Dados Filtrados")

st.dataframe(df_filtrado)
