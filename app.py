import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")


st.title("📊 Análise de Tempo de Espera")
st.markdown("*A unidade de tempo utilizada: Minutos *")

df=pd.read_excel('dados.xlsx')
df_excel_original = df.copy()
df_gantt = df_excel_original.copy()

df_gantt = df_gantt.sort_values(by="Servico")
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
    fig_espera = px.box(df, y="Total Espera segundos", 
                        title="Tempo de Espera",
                        labels={"Total Espera segundos": "Minutos"})
    fig_espera.update_layout(showlegend=False)
    st.plotly_chart(fig_espera, use_container_width=True)

with graf2:
    fig_atend = px.box(df, y="Total Atendimento segundos", 
                       title="Tempo de Atendimento",
                       labels={"Total Atendimento segundos": "Minutos", "Servico": "Serviço"})
    fig_atend.update_layout(showlegend=False)
    st.plotly_chart(fig_atend, use_container_width=True)

with graf3:
    fig_proc = px.box(df, y="Tempo processo", 
                      title="Tempo Total Processo",
                      labels={"Tempo processo": "Minutos", "Servico": "Serviço"})
    fig_proc.update_layout(showlegend=False)
    st.plotly_chart(fig_proc, use_container_width=True)
    
# ----------------- NOVA SEÇÃO: GRÁFICO DE DISPERSÃO (PICO POR HORÁRIO) -----------------
st.markdown("---")
st.subheader("Tempo de Espera por Horário de Entrada")

# 1. TRATAMENTO DOS DADOS: Converte para string apenas para garantir a ordenação no eixo X
df['hora_str'] = df['hora'].astype(str)

# Ordenamos o DataFrame para que o gráfico comece na madrugada e vá até a noite
df_ordenado_hora = df.sort_values(by='hora_str')


# 2. CRIANDO O GRÁFICO DE DISPERSÃO (Tempo de espera)
fig_dispersao_entrada = px.scatter(
    df_ordenado_hora, 
    x="hora_str", # <-- Mudamos aqui para usar a coluna de texto ordenada
    y="Total Espera segundos",
    title="Relação: Horário de Entrada vs. Tempo de Espera",
    labels={"hora_str": "Horário de Entrada", "Total Espera segundos": "Tempo de Espera (Minutos)"}, 
    opacity=0.6,     
    hover_data=["Servico"] 
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
    y="Total Atendimento segundos",
    title="Relação: Horário de Entrada vs. Tempo de Atendimento",
    labels={"hora_str": "Horário de Entrada", "Total Atendimento segundos": "Tempo de Atendimento (Minutos)"}, 
    opacity=0.6,     
    hover_data=["Servico"] 
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
    hover_data=["Servico"] 
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
st.subheader("Linha do Tempo e Jornada do Atendimento (Gantt)")



#campo de seleção e filtro dos dados
Dias=st.multiselect("Selecione uma data para análise da linha do tempo",df_gantt["data"].unique())
if Dias:
    df_gantt=df_gantt[df_gantt["data"].isin(Dias)]
    df_gantt = df_gantt.sort_values(by="data")
    Servicos=st.multiselect("Selecione o tipo de Serviço",df_gantt["Servico"].unique())
if Servicos:
    df_gantt=df_gantt[df_gantt["Servico"].isin(Servicos)]

st.metric("Frequência", f"{df_gantt['Servico'].count():,}")

# Garantimos que a data e a hora de entrada se unam em um formato de tempo real (Timestamp)
df_gantt['Inicio_Espera'] = pd.to_datetime(df_gantt['Chegada'], format='mixed')

# Calculamos o momento exato em que o atendimento começou (Somando a Entrada + Tempo de Espera)
df_gantt['Inicio_Atendimento'] = df_gantt['Inicio_Espera'] + pd.to_timedelta(df_gantt['Total Espera segundos'], unit='m')
# Calculamos o momento exato em que o processo terminou (Somando o início do atendimento + tempo de atendimento)
df_gantt['Fim_Processo'] = df_gantt['Inicio_Atendimento'] + pd.to_timedelta(df_gantt['Total Atendimento segundos'], unit='m')

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

# Nota: Substitua 'NCE001' abaixo pelo nome exato da sua primeira coluna (ID do Paciente / Senha)
# Supondo que a primeira coluna no seu df chame-se 'Senha' ou 'Id'
nome_coluna_id = df_linha_tempo.columns[0] 

# 3. CONSTRUINDO O GRÁFICO DE LINHA DO TEMPO
fig_gantt = px.timeline(
    df_linha_tempo, 
    x_start="Inicio", 
    x_end="Fim", 
    y=nome_coluna_id,           # Cada linha do gráfico será um paciente único (ex: NCE001, NCE002)
    color="Etapa Do Processo",  # Azul para Espera, Vermelho/Verde para Atendimento
    title="Linha do Tempo da Jornada por Paciente",
    labels={"Etapa Do Processo": "Fase", nome_coluna_id: "Código Paciente"},
    hover_data=["Guiche", "Servico"], # Mostra o guichê e o serviço ao passar o mouse
    color_discrete_map={"Espera": "#EF553B", "Atendimento": "#00CC96"} # Cores customizadas
)

# Inverte o eixo Y para que o primeiro paciente do dia (ex: NCE001) apareça no topo do gráfico
fig_gantt.update_yaxes(autorange="reversed")

# Configurações de layout
fig_gantt.update_layout(
    xaxis_title="Horário do Dia",
    legend_title_text="Legenda",
)

st.plotly_chart(fig_gantt, use_container_width=True)
