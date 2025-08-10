import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações da página
st.set_page_config(page_title="Dashboard Alura", layout="wide", page_icon=":bar_chart:")

# carregamento de dados 
df = pd.read_csv("dados-imersao-final.csv")   

# Barra Lateral
st.sidebar.header("Filtros")

# Filtros de Ano
ano_disponiveis = sorted(df["ano"].unique())
ano_selecionado = st.sidebar.multiselect("Ano", ano_disponiveis, default=ano_disponiveis)

# Filtro de Senioridade
senioridade_disponiveis = sorted(df["senioridade"].unique())
senioridade_selecionadas = st.sidebar.multiselect("Senioridade", senioridade_disponiveis, default=senioridade_disponiveis)

# Filtro por Tipo de Contrato
contratos_disponiveis = sorted(df["contrato"].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

#Filtro por tamanho da empresa 
tamanhos_disponiveis = sorted(df["tamanho_empresa"].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# Filtragem do DataFrame
df_filtrado = df[
    (df["ano"].isin(ano_selecionado)) &
    (df["senioridade"].isin(senioridade_selecionadas)) &
    (df["contrato"].isin(contratos_selecionados)) &
    (df["tamanho_empresa"].isin(tamanhos_selecionados))
]

# Conteudo Principal
st.title("Dashboard de Análise Salarial")
st.markdown("## Análise Salarial dos Profissionais de Ciência de Dados")

# Metricas Principais (KPI)
st.subheader("Métricas gerais (Salario Anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado["usd"].mean()
    salario_maximo = df_filtrado["usd"].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
else:
    salario_medio,salario_mediano,salario_maximo, total_registros, cargo_mais_comum = 0, 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário Médio", f"${salario_medio:,.2f}")
col2.metric("Salário Máximo", f"${salario_maximo:,.2f}")
col3.metric("Total de Registros", f"{total_registros}")
col4.metric("Cargo Mais Comum", cargo_mais_frequente)

st.markdown("---")

# Gráfico de Distribuição Salarial  
# Analises Visuais com plotly
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby("cargo")["usd"].mean().nlargest(10).sort_values(ascending=True).reset_index()
        graficos_cargos = px.bar(
            top_cargos,
            x="usd",
            y="cargo",
            orientation="h",
            title="Top 10 Cargos com Maior Salário Médio",
            labels={'usd': 'Média Salarial (USD)', 'cargo': ''}
        )

        graficos_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(graficos_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibição.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x="usd",
            nbins=30,
            title="Distribuição Salarial",
            labels={'usd': 'Faixa salarial (USD)', 'count': ''}
            )
        grafico_hist.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibição.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado["remoto"].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho','quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção de Trabalho Remoto',
            hole=0.5
        )
        grafico_remoto.update_traces(textposition='inside', textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibição.")

with col_graf4:
    if not df_filtrado.empty:
        if not df_filtrado.empty:
            df_ds = df_filtrado[df_filtrado["cargo"] == "Data Scientist"]
            media_ds_pais = df_ds.groupby("residencia_iso3")["usd"].mean().reset_index()
            grafico_paises = px.choropleth(media_ds_pais,
                locations='residencia_iso3',
                color='usd',
                color_continuous_scale='rdyLgn',
                title='Salário médio de Cientista de Dados por país',
                labels={'usd': 'Média Salarial (USD)', 'residencia_iso3': 'País'})
            grafico_paises.update_layout(title_x=0.1)
            st.plotly_chart(grafico_paises, use_container_width=True)

# Tabela de Dados Detalhados 
st.subheader("Tabela de Dados Detalhados")
st.dataframe(df_filtrado)
