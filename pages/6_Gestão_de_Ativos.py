import yfinance as yf
import json
import streamlit as st
from os import path
import pandas as pd
import os

st.set_page_config(
    page_title="Gestão de Ativos",
    page_icon="📈",
)

st.image('logo.png', caption=None, width=595, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
st.header("Gestão de Ativos")

model = st.selectbox("Selecione o portfólio modelo que deseja gerir:", ['Ações', 'Renda Fixa', 'Fundos Imobiliários', 'REITs', 'Stocks'])

if model == 'Fundos Imobiliários':
    st.subheader('Fundos Imobiliários')
    folder_path = "strategic_portfolios"
    file_name = "core_real_estate_br.json"

    # Caminho completo do arquivo JSON
    file_path = os.path.join(folder_path, file_name)
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)

    management = st.radio(
        'Selecione o tipo de alteração que deseja realizar:',
        ('Incluir novo ativo', 'Remover um ativo', 'Alterar a alocação'))

    if management == 'Incluir novo ativo':
        # Inserir novo registro em portfolio_file_path
        st.subheader('Insira os dados do ativo a ser incluído:')
        ticker_input = st.text_input("Informe o ticker do ativo: ")
        weight_input = st.text_input('Informe o peso do ativo:')
        segment_input = st.selectbox('Informe o segmento do ativo:', ['Recebíveis', 'Logístico e Industrial', 'Escritórios', 'Fundos de Fundos', 'Renda Urbena', 'Shoppings'])

        if ticker_input and weight_input and segment_input:
            ticker = str(ticker_input)
            weight = float(weight_input)
            segment = str(segment_input)
        
        if st.button('Enviar'):
            # Lendo o arquivo JSON existente
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Verificando se o ticker já existe no JSON
            ticker_exists = False
            for item in data:
                if item['Ticker'] == ticker:
                    item['Alocação Alvo'] = weight
                    item['Segmento'] = segment
                    ticker_exists = True
                    break
            
            # Se o ticker não existir, adiciona um novo registro aos dados existentes
            if not ticker_exists:
                data.append({
                    'Ticker': ticker,
                    'Alocação Alvo': weight,
                    'Segmento': segment,               
                })
            
            # Escrevendo o arquivo JSON com todos os registros digitados
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
                st.write('Inclusão de ativo realizada com sucesso.')
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            
    elif management == 'Remover um ativo':
        # Inserir novo registro em portfolio_file_path
        st.subheader('Insira os dados do ativo a ser removido do portfólio:')
        ticker_input = st.text_input("Informe o ticker do ativo: ")

        if ticker_input:
            ticker = str(ticker_input)

        if st.button('Enviar'):
            # Lendo o arquivo JSON existente
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Cria uma cópia do dicionário original
            data_copy = data.copy()

            # Itera sobre a cópia para evitar problemas de alteração durante a iteração
            for item in data_copy:
                if item['Ticker'] == ticker:
                    data.remove(item)

            # Escreve o arquivo JSON atualizado
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
                st.write('Ativo removido com sucesso.')
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            df = pd.DataFrame(data)

    elif management == 'Alterar a alocação':
        # Inserir novo registro em portfolio_file_path
        st.subheader('Insira os dados do ativo a ser alterado:')
        ticker_input = st.text_input("Informe o ticker do ativo: ")
        weight_input = st.text_input('Informe o novo peso do ativo:')

        if ticker_input and weight_input:
            ticker = str(ticker_input)
            weight = float(weight_input)
        
        if st.button('Enviar'):
            # Lendo o arquivo JSON existente
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Verificando se o ticker já existe no JSON
            ticker_exists = False
            for item in data:
                if item['Ticker'] == ticker:
                    item['Alocação Alvo'] = weight
                    ticker_exists = True
                    break
            
            if not ticker_exists:
                st.write('Ativo inexistente.')

            # Escrevendo o arquivo JSON com todos os registros digitados
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
                st.write('Alocação alterada com sucesso.')
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            df = pd.DataFrame(data)

    # Calcular a soma da "Alocação Alvo" para cada "Segmento"
    df['Alocação no segmento (%)'] = df.groupby('Segmento')['Alocação Alvo'].transform('sum')
    df = df.sort_values('Ticker', ascending=True)
    total = df['Alocação Alvo'].sum()
    total_formatted = format(total, ".4f")
    total_float = float(total_formatted)

    diff_decimal_above = 1 - total_float
    diff_percent_above = diff_decimal_above * 100
    diff_percent_above_formatted = format(diff_percent_above, ".1f")

    diff_decimal_below = 1 - total_float
    diff_percent_below = diff_decimal_above * 100
    diff_percent_below_formatted = format(diff_percent_above, ".1f")
    
    if total_float > 1:
        st.write(f'A alocação alvo do portfólio é superior a 100%. Ajuste-o em {diff_percent_above_formatted} p.p.')

    if total_float < 1:
        st.write(f'A alocação alvo do portfólio é inferior a 100%. Ajuste-o em + {diff_percent_below_formatted} p.p.')

if model == 'Ações':
    st.subheader('Ações')
    folder_path = "strategic_portfolios"
    file_name = "core_stocks.json"

    # Caminho completo do arquivo JSON
    file_path = os.path.join(folder_path, file_name)
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)

html = df.to_html(index=False)

# Adicionar estilo CSS para ajustar o tamanho das colunas
html = """
<style>
table {
width: 100%;
border-collapse: collapse;
}

th, td {
padding: 8px;
text-align: left;
white-space: nowrap;
overflow: hidden;
text-overflow: ellipsis;
}

/* Ajuste manual das larguras das colunas */
th:nth-child(1), td:nth-child(1) {
width: 20%;
}

th:nth-child(2), td:nth-child(2) {
width: 30%;
}

th:nth-child(3), td:nth-child(3) {
width: 50%;
}
</style>
""" + html

# Exibir o HTML no Streamlit
st.markdown(html, unsafe_allow_html=True)