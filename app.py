import pandas as pd
import streamlit as st
import plotly.express as px

#configurando o layout da página
st.set_page_config(layout="wide")


st.title("📊 Análise de Tempo de Espera")
st.markdown("*A unidade de tempo utilizada: Minutos *")

df=pd.read_excel('dados.xlsx')
df = df.sort_values(by="Servico")

#campo de seleçã e filtro dos dados
Servicos=st.multiselect("Selecione o tipo de Serviço",df["Servico"].unique())

st.subheader("Tempo de Espera") # Subtítulo Grande (Seção)
if Servicos:
    df=df[df["Servico"].isin(Servicos)]

#métricas 
# Cria 7 colunas lado a lado
col0, col1, col2, col3, col4, col5, col6, col7 = st.columns(8)


# Coloca cada métrica em sua respectiva coluna
with col0:
    st.metric("Frequência", f"{df['Total Espera segundos'].count():,}")
with col1:
    st.metric("Total",f"{df['Total Espera segundos'].sum():,.2f}")
with col2:
    st.metric("Média",f"{df['Total Espera segundos'].mean():,.2f}")
with col3:
    st.metric("Desvio Padrão", f"{df['Total Espera segundos'].std():,.2f}")
with col4:
    st.metric("Mediana", f"{df['Total Espera segundos'].median():,.2f}")
with col5:
    st.metric("Mínimo", f"{df['Total Espera segundos'].min():,.2f}")
with col6:
    st.metric("Máximo", f"{df['Total Espera segundos'].max():,.2f}")
with col7:
    st.metric("Amplitude", f"{df['Total Espera segundos'].max()-df['Total Espera segundos'].min():,.2f}")

st.subheader("Tempo Atendimento") # Subtítulo Grande (Seção)
#if Servicos:
#    df=df[df["Servico"].isin(Servicos)]

#métricas 
# Cria 7 colunas lado a lado
col0, col1, col2, col3, col4, col5, col6, col7 = st.columns(8)
# Coloca cada métrica em sua respectiva coluna
with col0:
    st.metric("Frequência", f"{df['Total Atendimento segundos'].count():,}")
with col1:
    st.metric("Total",f"{df['Total Atendimento segundos'].sum():,.2f}")
with col2:
    st.metric("Tempo médio",f"{df['Total Atendimento segundos'].mean():,.2f}")
with col3:
    st.metric("Desvio Padrão", f"{df['Total Atendimento segundos'].std():,.2f}")
with col4:
    st.metric("Mediana", f"{df['Total Atendimento segundos'].median():,.2f}")
with col5:
    st.metric("Mínimo", f"{df['Total Atendimento segundos'].min():,.2f}")
with col6:
    st.metric("Máximo", f"{df['Total Atendimento segundos'].max():,.2f}")
with col7:
    st.metric("Amplitude", f"{df['Total Atendimento segundos'].max()-df['Total Atendimento segundos'].min():,.2f}")

st.subheader("Tempo Total Processo") # Subtítulo Grande (Seção)
#if Servicos:
#    df=df[df["Servico"].isin(Servicos)]

#métricas 
# Cria 7 colunas lado a lado
col0, col1, col2, col3, col4, col5, col6, col7 = st.columns(8)
# Coloca cada métrica em sua respectiva coluna
with col0:
    st.metric("Frequência", f"{df['Tempo processo'].count():,}")
with col1:
    st.metric("Total",f"{df['Tempo processo'].sum():,.2f}")
with col2:
    st.metric("Média",f"{df['Tempo processo'].mean():,.2f}")
with col3:
    st.metric("Desvio Padrão", f"{df['Tempo processo'].std():,.2f}")
with col4:
    st.metric("Mediana", f"{df['Tempo processo'].median():,.2f}")
with col5:
    st.metric("Mínimo", f"{df['Tempo processo'].min():,.2f}")
with col6:
    st.metric("Máximo", f"{df['Tempo processo'].max():,.2f}")
with col7:
    st.metric("Amplitude", f"{df['Tempo processo'].max()-df['Tempo processo'].min():,.2f}")

# ----------------- NOVA SEÇÃO: GRÁFICOS (BOXPLOTS) -----------------
st.markdown("---") # Linha divisória horizontal
st.subheader("📊 Distribuição e Outliers (Boxplot)")

# Criando 3 colunas para colocar os gráficos lado a lado
graf1, graf2, graf3 = st.columns(3)

with graf1:
    # x="Servico" faz criar um boxplot para cada serviço selecionado lado a lado
    fig_espera = px.box(df, x="Servico", y="Total Espera segundos", 
                        title="Tempo de Espera",
                        labels={"Total Espera segundos": "Minutos", "Servico": "Serviço"},
                        color="Servico") # Cores diferentes por serviço
    fig_espera.update_layout(showlegend=False)
    st.plotly_chart(fig_espera, use_container_width=True)

with graf2:
    fig_atend = px.box(df, x="Servico", y="Total Atendimento segundos", 
                       title="Distribuição: Tempo de Atendimento",
                       labels={"Total Atendimento segundos": "Minutos", "Servico": "Serviço"},
                       color="Servico")
    fig_atend.update_layout(showlegend=False)
    st.plotly_chart(fig_atend, use_container_width=True)

with graf3:
    fig_proc = px.box(df, x="Servico", y="Tempo processo", 
                      title="Distribuição: Tempo Total Processo",
                      labels={"Tempo processo": "Minutos", "Servico": "Serviço"},
                      color="Servico")
    fig_proc.update_layout(showlegend=False)
    st.plotly_chart(fig_proc, use_container_width=True)
