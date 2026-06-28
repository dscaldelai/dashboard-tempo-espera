import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")


st.title("📊 Análise de Tempo")
st.markdown("*A unidade de tempo utilizada: Minutos *")

df=pd.read_excel('dados2.xlsx')
df_excel_original = df.copy()

df1 = df.sort_values(by="Servico2")

#campo de seleção e filtro dos dados
Servicos=st.multiselect("Selecione um serviço",df1["Servico2"].unique())
Tipos = []
if Servicos:
    df1=df1[df1["Servico2"].isin(Servicos)]
    df1 = df1.sort_values(by="Servico2")
    Tipos=st.multiselect("Selecione o tipo de atendimento",df1["Tipo"].unique())
if Tipos:
    df1=df1[df1["Tipo"].isin(Tipos)]
    


#campo de seleçã e filtro dos dados
#Servicos=st.multiselect("Selecione o tipo de Serviço",df["Servico2"].unique())

#st.subheader("Tempo de Espera") # Subtítulo Grande (Seção)


#if Servicos:
#    df=df[df["Servico"].isin(Servicos)]

#métricas 
# Cria 7 colunas lado a lado
col0, col1, col2, col3, col4, col5, col6, col7 = st.columns(8)


# Coloca cada métrica em sua respectiva coluna
with col0:
    st.metric("Frequência", f"{df1['Total Espera2'].count():,}")
with col1:
    st.metric("Total",f"{df1['Total Espera2'].sum():,.2f}")
with col2:
    st.metric("Média",f"{df1['Total Espera2'].mean():,.2f}")
with col3:
    st.metric("Desvio Padrão", f"{df1['Total Espera2'].std():,.2f}")
with col4:
    st.metric("Mediana", f"{df1['Total Espera2'].median():,.2f}")
with col5:
    st.metric("Mínimo", f"{df1['Total Espera2'].min():,.2f}")
with col6:
    st.metric("Máximo", f"{df1['Total Espera2'].max():,.2f}")
with col7:
    st.metric("Amplitude", f"{df1['Total Espera2'].max()-df1['Total Espera2'].min():,.2f}")

st.subheader("Tempo Atendimento") # Subtítulo Grande (Seção)
#if Servicos:
#    df=df[df["Servico"].isin(Servicos)]

#métricas 
# Cria 7 colunas lado a lado
col0, col1, col2, col3, col4, col5, col6, col7 = st.columns(8)
# Coloca cada métrica em sua respectiva coluna
with col0:
    st.metric("Frequência", f"{df1['Total Atendimento2'].count():,}")
with col1:
    st.metric("Total",f"{df1['Total Atendimento2'].sum():,.2f}")
with col2:
    st.metric("Tempo médio",f"{df1['Total Atendimento2'].mean():,.2f}")
with col3:
    st.metric("Desvio Padrão", f"{df1['Total Atendimento2'].std():,.2f}")
with col4:
    st.metric("Mediana", f"{df1['Total Atendimento2'].median():,.2f}")
with col5:
    st.metric("Mínimo", f"{df1['Total Atendimento2'].min():,.2f}")
with col6:
    st.metric("Máximo", f"{df1['Total Atendimento2'].max():,.2f}")
with col7:
    st.metric("Amplitude", f"{df1['Total Atendimento2'].max()-df1['Total Atendimento2'].min():,.2f}")

st.subheader("Tempo Total Processo") # Subtítulo Grande (Seção)
#if Servicos:
#    df=df[df["Servico"].isin(Servicos)]

#métricas 
# Cria 7 colunas lado a lado
col0, col1, col2, col3, col4, col5, col6, col7 = st.columns(8)
# Coloca cada métrica em sua respectiva coluna
with col0:
    st.metric("Frequência", f"{df1['Tempo processo'].count():,}")
with col1:
    st.metric("Total",f"{df1['Tempo processo'].sum():,.2f}")
with col2:
    st.metric("Média",f"{df1['Tempo processo'].mean():,.2f}")
with col3:
    st.metric("Desvio Padrão", f"{df1['Tempo processo'].std():,.2f}")
with col4:
    st.metric("Mediana", f"{df1['Tempo processo'].median():,.2f}")
with col5:
    st.metric("Mínimo", f"{df1['Tempo processo'].min():,.2f}")
with col6:
    st.metric("Máximo", f"{df1['Tempo processo'].max():,.2f}")
with col7:
    st.metric("Amplitude", f"{df1['Tempo processo'].max()-df1['Tempo processo'].min():,.2f}")

# ----------------- NOVA SEÇÃO: GRÁFICOS (BOXPLOTS) -----------------
st.markdown("---") # Linha divisória horizontal
st.subheader("📊 Distribuição e Outliers (Boxplot)")

# Criando 3 colunas para colocar os gráficos lado a lado
graf1, graf2, graf3 = st.columns(3)

with graf1:
    fig_espera = px.box(df1, y="Total Espera2",
                        title="Distribuição: Tempo de Espera (Geral)",
                        labels={"Total Espera segundos": "Minutos"})
    fig_espera.update_layout(showlegend=False)
    st.plotly_chart(fig_espera, use_container_width=True)

with graf2:
    fig_atend = px.box(df1, y="Total Atendimento2", 
                       title="Distribuição: Tempo de Atendimento",
                       labels={"Total Atendimento segundos": "Minutos", "Servico": "Serviço"})
    fig_atend.update_layout(showlegend=False)
    st.plotly_chart(fig_atend, use_container_width=True)

with graf3:
    fig_proc = px.box(df1, y="Tempo processo", 
                      title="Distribuição: Tempo Total Processo",
                      labels={"Tempo processo": "Minutos", "Servico2": "Serviço"})
    fig_proc.update_layout(showlegend=False)
    st.plotly_chart(fig_proc, use_container_width=True)
    
# ----------------- NOVA SEÇÃO: GRÁFICO DE DISPERSÃO (PICO POR HORÁRIO) -----------------
st.markdown("---")
st.subheader("Tempo de Espera por Horário de Entrada")

# 1. TRATAMENTO DOS DADOS: Converte para string apenas para garantir a ordenação no eixo X
df1['hora_str'] = df1['hora'].astype(str)

# Ordenamos o DataFrame para que o gráfico comece na madrugada e vá até a noite
df_ordenado_hora = df1.sort_values(by='hora_str')


# 2. CRIANDO O GRÁFICO DE DISPERSÃO (Tempo de espera)
fig_dispersao_entrada = px.scatter(
    df_ordenado_hora, 
    x="hora_str", # <-- Mudamos aqui para usar a coluna de texto ordenada
    y="Total Espera2",
    title="Relação: Horário de Entrada vs. Tempo de Espera",
    labels={"hora_str": "Horário de Entrada", "Total Espera segundos": "Tempo de Espera (Minutos)"}, 
    opacity=0.6,     
    hover_data=["Servico2"] 
)

# Ajustes no layout para o gráfico ficar mais limpo
fig_dispersao_entrada.update_layout(
    xaxis_tickangle=-45, # Inclina os horários no eixo X para não embolarem se houverem muitos
    legend_title_text="Serviço" # Dá um nome bonito para a legenda lateral
)

# Renderiza o gráfico ocupando a largura total da tela
st.plotly_chart(fig_dispersao_entrada, use_container_width=True)


st.markdown("---")
st.subheader("Tempo de Atendimento por Horário de Entrada")

# 2. CRIANDO O GRÁFICO DE DISPERSÃO (Tempo de atendimento)
fig_dispersao_atendimento = px.scatter(
    df_ordenado_hora, 
    x="hora_str", # <-- Mudamos aqui para usar a coluna de texto ordenada
    y="Total Atendimento2",
    title="Relação: Horário de Entrada vs. Tempo de Atendimento",
    labels={"hora_str": "Horário de Entrada", "Total Atendimento segundos": "Tempo de Atendimento (Minutos)"}, 
    opacity=0.6,     
    hover_data=["Servico2"] 
)

# Ajustes no layout para o gráfico ficar mais limpo
fig_dispersao_atendimento.update_layout(
    xaxis_tickangle=-45, # Inclina os horários no eixo X para não embolarem se houverem muitos
    legend_title_text="Serviço" # Dá um nome bonito para a legenda lateral
)

# Renderiza o gráfico ocupando a largura total da tela
st.plotly_chart(fig_dispersao_atendimento, use_container_width=True)


st.markdown("---")
st.subheader("Tempo total no processo por Horário de Entrada")

# 2. CRIANDO O GRÁFICO DE DISPERSÃO (Tempo de atendimento)
fig_dispersao_processo = px.scatter(
    df_ordenado_hora, 
    x="hora_str", # <-- Mudamos aqui para usar a coluna de texto ordenada
    y="Tempo processo",
    title="Relação: Horário de Entrada vs. Tempo no Processo",
    labels={"hora_str": "Horário de Entrada", "Tempo processo": "Tempo no Processo (Minutos)"}, 
    opacity=0.6,     
    hover_data=["Servico2"] 
)

# Ajustes no layout para o gráfico ficar mais limpo
fig_dispersao_processo.update_layout(
    xaxis_tickangle=-45, # Inclina os horários no eixo X para não embolarem se houverem muitos
    legend_title_text="Serviço" # Dá um nome bonito para a legenda lateral
)

# Renderiza o gráfico ocupando a largura total da tela
st.plotly_chart(fig_dispersao_processo, use_container_width=True)




# ----------------- NOVA SEÇÃO: JORNADA DO PACIENTE (GRÁFICO DE GANTT) -----------------
st.markdown("---")
st.subheader("Linha do Tempo e Jornada do Atendimento")



# 1. TRATAMENTO DOS DADOS PARA CRIAR O CRONOGRAMA
# Criar cópias para não afetar o restante do dashboard
df_gantt = df_excel_original.copy()

# Seleção de Serviço
Servicos = st.multiselect(
    "Selecione o tipo de Serviço",
    sorted(df_gantt["Servico2"].unique())
)

if Servicos:
    df_gantt = df_gantt[df_gantt["Servico2"].isin(Servicos)]

# Seleção da Data
Dia = st.selectbox(
    "Selecione uma data para análise da linha do tempo",
    sorted(df_gantt["data"].unique())
)

df_gantt = df_gantt[df_gantt["data"] == Dia]

# Seleção do Atendente
Atendentes = st.multiselect(
    "Selecione o(s) atendente(s)",
    sorted(df_gantt["Cod.Atendente"].dropna().unique())
)

if Atendentes:
    df_gantt = df_gantt[df_gantt["Cod.Atendente"].isin(Atendentes)]

# Ordenação final
df_gantt = df_gantt.sort_values(by="hora")

st.metric("Frequência", f"{df_gantt['Servico2'].count():,}")


# Garantimos que a data e a hora de entrada se unam em um formato de tempo real (Timestamp)
df_gantt['Inicio_Espera'] = pd.to_datetime(df_gantt['Chegada'], format='mixed')

# Calculamos o momento exato em que o atendimento começou (Somando a Entrada + Tempo de Espera)
df_gantt['Inicio_Atendimento'] = df_gantt['Inicio_Espera'] + pd.to_timedelta(df_gantt['Total Espera2'], unit='m')
# Calculamos o momento exato em que o processo terminou (Somando o início do atendimento + tempo de atendimento)
df_gantt['Fim_Processo'] = df_gantt['Inicio_Atendimento'] + pd.to_timedelta(df_gantt['Total Atendimento2'], unit='m')
# intervalo completo da análise

inicio = df_gantt["Inicio_Espera"].min().floor("min")
fim = df_gantt["Fim_Processo"].max().ceil("min")

resultado = []



timeline = pd.date_range(
    start=inicio,
    end=fim,
    freq="1min"
)

# 2. MODELANDO OS DADOS NO FORMATO DO GRÁFICO (LINHA DO TEMPO)
# Para fazer o Gantt mostrar duas barras na mesma linha (Espera e Atendimento), duplicamos as linhas
etapa_espera = df_gantt.copy()
etapa_espera['Inicio'] = etapa_espera['Inicio_Espera']
etapa_espera['Fim'] = etapa_espera['Inicio_Atendimento']
etapa_espera['Etapa Do Processo'] = 'Espera'

etapa_atend = df_gantt.copy()
etapa_atend['Inicio'] = etapa_atend['Inicio_Atendimento']
etapa_atend['Fim'] = etapa_atend['Fim_Processo']
etapa_atend['Etapa Do Processo'] = 'Atendimento'

# Juntamos as duas etapas de volta em um único bloco de dados
df_linha_tempo = pd.concat([etapa_espera, etapa_atend])


for instante in timeline:

    fila = (
        (df_gantt["Inicio_Espera"] <= instante)
        &
        (instante < df_gantt["Inicio_Atendimento"])
    ).sum()

    atendimento = (
        (df_gantt["Inicio_Atendimento"] <= instante)
        &
        (instante < df_gantt["Fim_Processo"])
    ).sum()

    resultado.append(
        {
            "Momento": instante,
            "Fila": fila,
            "Atendimento": atendimento
        }
    )

df_fluxo = pd.DataFrame(resultado)


df_fluxo["Atendimento_neg"] = -df_fluxo["Atendimento"]

fig_fluxo = px.bar(
    df_fluxo,
    x="Momento",
    y=["Fila", "Atendimento_neg"],
    title="Pacientes na espera e no atendimento"
)

fig_fluxo.update_layout(
    barmode="overlay",
    xaxis_title="Horário",
    yaxis_title="Quantidade de Pacientes"
)

st.plotly_chart(
    fig_fluxo,
    use_container_width=True
)


# 3. MODELANDO AS FREQUENCIAS DE ATENDIMENTO POR ATENDENTE E TIPO DE SERVIÇO
# Para fazer o Gantt mostrar duas barras na mesma linha (Espera e Atendimento), duplicamos as linhas
st.markdown("---")
st.subheader("Análise de tempo por atendente")

df2 = df_excel_original.sort_values(by="Servico2")

#campo de seleção e filtro dos dados
Atend=st.multiselect("Selecione um atendente",df2["Cod.Atendente"].unique())
Servicos_atend = []
if Atend:
    df2=df2[df2["Cod.Atendente"].isin(Atend)]
    df2 = df2.sort_values(by="Cod.Atendente")
    Servicos_atend = st.multiselect("Selecione o tipo de Serviço",df2["Servico2"].unique(),key="servicos_atendente")   
if Servicos_atend:
    df2=df2[df2["Servico2"].isin(Servicos_atend)]


freq_servicos = (
    df2.groupby(["Cod.Atendente", "Servico2"])
       .size()
       .reset_index(name="Frequencia")
)

fig_freq = px.bar(
    freq_servicos,
    x="Servico2",
    y="Frequencia",
    color="Cod.Atendente",
    barmode="group",
    title="Quantidade de atendimentos realizados por atendente",
    labels={
        "Servico2": "Tipo de Serviço",
        "Frequencia": "Quantidade",
        "Cod.Atendente": "Atendente"
    }
)

st.plotly_chart(
    fig_freq,
    use_container_width=True
)





st.markdown("---") # Linha divisória horizontal


freq_dias = (
    df2.groupby(["data", "Cod.Atendente"])
       .size()
       .reset_index(name="Frequencia")
)

fig_dias = px.bar(
    freq_dias,
    x="data",
    y="Frequencia",
    color="Cod.Atendente",
    barmode="group",
    title="Quantidade de atendimentos por dia e por atendente",
    labels={
        "data": "Data",
        "Frequencia": "Quantidade",
        "Cod.Atendente": "Atendente"
    }
)

st.plotly_chart(
    fig_dias,
    use_container_width=True
)

st.markdown("---") # Linha divisória horizontal


if Atend:
    st.markdown(
        f"### Medidas descritivas dos atendimentos realizados por: **{', '.join(map(str, Atend))}**"
    )
else:
    st.markdown(
        "### Medidas descritivas dos atendimentos realizados por **todos os atendentes**"
    )
    
    
#métricas 

st.subheader("Tempo de Espera") # Subtítulo Grande (Seção)

# Cria 7 colunas lado a lado
col0, col1, col2, col3, col4, col5, col6, col7 = st.columns(8)


# Coloca cada métrica em sua respectiva coluna
with col0:
    st.metric("Frequência", f"{df2['Total Espera2'].count():,}")
with col1:
    st.metric("Total",f"{df2['Total Espera2'].sum():,.2f}")
with col2:
    st.metric("Média",f"{df2['Total Espera2'].mean():,.2f}")
with col3:
    st.metric("Desvio Padrão", f"{df2['Total Espera2'].std():,.2f}")
with col4:
    st.metric("Mediana", f"{df2['Total Espera2'].median():,.2f}")
with col5:
    st.metric("Mínimo", f"{df2['Total Espera2'].min():,.2f}")
with col6:
    st.metric("Máximo", f"{df2['Total Espera2'].max():,.2f}")
with col7:
    st.metric("Amplitude", f"{df2['Total Espera2'].max()-df2['Total Espera2'].min():,.2f}")

st.subheader("Tempo Atendimento") # Subtítulo Grande (Seção)
#if Servicos:
#    df=df[df["Servico"].isin(Servicos)]

#métricas 
# Cria 7 colunas lado a lado
col0, col1, col2, col3, col4, col5, col6, col7 = st.columns(8)
# Coloca cada métrica em sua respectiva coluna
with col0:
    st.metric("Frequência", f"{df2['Total Atendimento2'].count():,}")
with col1:
    st.metric("Total",f"{df2['Total Atendimento2'].sum():,.2f}")
with col2:
    st.metric("Tempo médio",f"{df2['Total Atendimento2'].mean():,.2f}")
with col3:
    st.metric("Desvio Padrão", f"{df2['Total Atendimento2'].std():,.2f}")
with col4:
    st.metric("Mediana", f"{df2['Total Atendimento2'].median():,.2f}")
with col5:
    st.metric("Mínimo", f"{df2['Total Atendimento2'].min():,.2f}")
with col6:
    st.metric("Máximo", f"{df2['Total Atendimento2'].max():,.2f}")
with col7:
    st.metric("Amplitude", f"{df2['Total Atendimento2'].max()-df2['Total Atendimento2'].min():,.2f}")

st.subheader("Tempo Total Processo") # Subtítulo Grande (Seção)
#if Servicos:
#    df=df[df["Servico"].isin(Servicos)]

#métricas 
# Cria 7 colunas lado a lado
col0, col1, col2, col3, col4, col5, col6, col7 = st.columns(8)
# Coloca cada métrica em sua respectiva coluna
with col0:
    st.metric("Frequência", f"{df2['Tempo processo'].count():,}")
with col1:
    st.metric("Total",f"{df2['Tempo processo'].sum():,.2f}")
with col2:
    st.metric("Média",f"{df2['Tempo processo'].mean():,.2f}")
with col3:
    st.metric("Desvio Padrão", f"{df2['Tempo processo'].std():,.2f}")
with col4:
    st.metric("Mediana", f"{df2['Tempo processo'].median():,.2f}")
with col5:
    st.metric("Mínimo", f"{df2['Tempo processo'].min():,.2f}")
with col6:
    st.metric("Máximo", f"{df2['Tempo processo'].max():,.2f}")
with col7:
    st.metric("Amplitude", f"{df2['Tempo processo'].max()-df2['Tempo processo'].min():,.2f}")
