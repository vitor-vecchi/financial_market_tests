import yfinance as yf
import json
import streamlit as st
from os import path
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as pc
import numpy as np
import plotly.express as px
import os

st.set_page_config(
    page_title="Análise do Perfil do Investidor",
    page_icon="📈",
)

st.image('logo.png', caption=None, width=595, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
st.markdown("# Análise do Perfil do Investidor")

cic = st.text_input("Digite o código de identificação do cliente para carregamento dos dados (Formato: CIC-NUM):")

st.markdown("", unsafe_allow_html=True)

temas = st.multiselect(label='Selecione as ferramentas a serem utilizadas:', options=['Perfil', 'Situação Financeira', 'Situação Patrimonial, Liquidez e Patrimônio', 'Gestão de Riscos', 'Relatório de Coleta de Dados'], key = '101')

if 'Perfil' in temas:
    sexo = st.radio(
    'Informe o sexo do cliente:',
    ('Masculino', 'Feminino'))

    if sexo == 'Masculino':
        art_min = 'o'
        art_mai = 'O'

    if sexo == 'Feminino':
        art_min = 'a'
        art_mai = 'A'

    profissao = st.radio(
    'Informe a(s) atividade(s) principal(is) exercida(s):', ('Celetista em empresa privada', 'Celetista em empresa pública', 'Servidor Público Municipal', 'Servidor Público Estadual', 'Servidor Público Federal', 'Cargo em Comissão', 'Função Gratificada', 'Profissional Liberal', 'Empresário'), key="102")

    def get_age():
        data_minima = datetime.date(1900, 1, 1)
        # Coletando a data de nascimento do usuário
        birthdate = st.date_input("Qual é a sua data de nascimento?", min_value=data_minima, key = '103')
        
        if birthdate:
            # Calculando a diferença entre a data atual e a data de nascimento
            
            if sexo == 'Masculino':
                idade_aposentadoria = 65

            if sexo == 'Feminino':
                idade_aposentadoria = 62

            if st.checkbox("Aplicar regra de transição"):
                idade_aposentadoria = st.number_input("Informe a idada aplicável à regra de transição", min_value=0, key = '104')

            today = datetime.date.today()
            age_calc = today - birthdate
            tempo_aposentadoria = datetime.timedelta(days=(idade_aposentadoria * 365)) - age_calc

            # Convertendo a idade em anos, meses e dias
            years_age = age_calc.days // 365
            remaining_days_age = age_calc.days % 365
            months_age = remaining_days_age // 30
            days_age = remaining_days_age % 30

            # Convertendo o tempo até a aposentadoria em anos, meses e dias
            years_retirement = tempo_aposentadoria.days // 365
            remaining_days_retirement = tempo_aposentadoria.days % 365
            months_retirement = remaining_days_retirement // 30
            days_retirement = remaining_days_retirement % 30

            # Formatando o resultado
            idade = f"{years_age} anos, {months_age} meses e {days_age} dias"
            retirement = f"{years_retirement} anos, {months_retirement} meses e {days_retirement} dias"

            # Exibindo o resultado
            st.write(f"A idade d{art_min} cliente é: {idade}.")
            st.write(f"Faltam {retirement} para {art_min} cliente se aposentar.")
    get_age()

### Gestão de Riscos
if 'Gestão de Riscos' in temas:
    st.subheader("Gestão de Riscos", divider='green')
    risk = st.slider("Ajuste o nível de risco (0 a 10):", min_value=0, max_value=10, key = '105')

### Situação Financeira
if 'Situação Financeira' in temas:
    st.subheader("Situação Financeira", divider='rainbow')
    dados = []
    instrucao_inicial_unica = False  # Variável de controle

    for i in range(12):
# Subtrair 11 meses da data atual
        data_atual = datetime.date.today()
        mes = data_atual - datetime.timedelta(days=30*(i))
        mes_atual = data_atual - datetime.timedelta(days=30)

# Formatar a data como "mês_ano" com underline e barra
        data_formatada_underline = mes.strftime("%m_%Y")
        data_formatada_barra = mes.strftime("%m/%Y")
        data_atual_formatada_barra = mes_atual.strftime("%m/%Y")

        if not instrucao_inicial_unica:  # Verifica se a mensagem já foi exibida
            # st.markdown("", unsafe_allow_html=True)
            st.subheader(
                f"Informe a renda auferida e os valores investidos nos últimos 12 meses ({data_formatada_barra} até {data_atual_formatada_barra})", 
                divider='rainbow')
            instrucao_inicial_unica = True  # Define a variável de controle como True

        wage_client = st.number_input(f'Informe a renda total líquida da família {data_formatada_barra}:', key=f"salario_{i}", step=100.0)
        savings = st.number_input(f'Informe o valor poupado em {data_formatada_barra}:', key=f"poupanca_{i}", step=100.0)
        st.markdown("", unsafe_allow_html=True)
        st.markdown("", unsafe_allow_html=True)
        st.markdown("", unsafe_allow_html=True)

        file_name = cic + ".json"
        folder_path = "client_data"

        file_path = os.path.join(folder_path, file_name)

        with open(file_path, 'r') as f:
            data = json.load(f)

        with open(file_path, 'w') as f:
            json.dump(dados, f, indent=4)       
            dados.append({"Mês/Ano": data_formatada_underline, "Renda Total": wage_client, "Valor Investido": savings})

        count =+ datetime.timedelta(days=12*30)
    # Exibir os dados

    for i in dados:
        st.write(i)

### Relatório de Coleta de Dados
if 'Relatório de Coleta de Dados' in temas:
        def report():
            st.subheader("Relatório de Coleta de Dados", divider='orange')
            file_name = cic + ".json"
            folder_path = "client_data"

            file_path = os.path.join(folder_path, file_name)

            if st.button('Carregar dados do cliente'):
                # Lendo o arquivo JSON
                archive_name = cic + '.json'
                with open(file_path, 'r') as f:
                    data = json.load(f)

            if st.button('Exibir o Perfil'):
                # Criando o DataFrame
                df = pd.DataFrame(dict(
                    r=[1, 5, 2, 2, 3, 7],
                    theta=['Propensão a riscos','Segurança','Investimentos no exterior',
                            'Necessidade previdenciária', 'Horizonte de tempo', 'Necessidade de Liquidez']))

                # Criando o gráfico polar
                fig = px.line_polar(df, r='r', theta='theta', line_close=True)

                # Exibindo o gráfico no Streamlit
                st.plotly_chart(fig)
        report()

