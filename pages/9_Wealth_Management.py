import yfinance as yf
import json
import streamlit as st
from os import path
import pandas as pd
import os
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Wealth Management",
    page_icon="📈",
)

st.image('logo.png', caption=None, width=595, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
st.header("Wealth Management")

st.subheader("Seleção de Portfólio")

def client_search():
    cic_search = st.text_input("Informe o nome ou código de identificação do cliente para consultar o cadastro no banco de dados (Formato: CIC-NUM):")
    if cic_search:
        # Nome do arquivo JSON e caminho da pasta
        clients_folder_path = "clients_registries"
        clients_file_name = "clients.json"

        # Caminho completo do arquivo JSON
        file_path = os.path.join(clients_folder_path, clients_file_name)

        # Verifica se o arquivo JSON existe
        if os.path.exists(file_path):
            # Lê o conteúdo do arquivo JSON
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Filtra os dados que correspondem à pesquisa (por código de identificação ou nome)
            filtered_data = [client for client in data if cic_search in client['Código de Identificação'] or cic_search in client['Nome']]

            # Exiba os clientes selecionados usando um checkbox
            if filtered_data:
                df = pd.DataFrame(filtered_data)
                # Converter o dataframe em HTML e remover a primeira coluna numerada
                html = df.to_html(index=False)

                # Exibir o HTML no Streamlit
                st.markdown(html, unsafe_allow_html=True)
                # Verificar se um cliente com o nome correspondente foi encontrado
                for client in filtered_data:
                    if cic_search == client['Nome']:
                        cic_search = client['Código de Identificação']
                        break  # Se encontrado, atualiza cic_search e sai do loop

            else:
                st.write("Nenhum registro encontrado para o código de identificação informado.")
        # else:
            # st.write("Selecione o cliente para prosseguir.")
        cic_search = client['Código de Identificação']

    if cic_search:
        def new_op(cic_search):
            portfolio_folder_path = "clients_portfolios"
            portfolio_file_name = cic_search + '_portfolio.json'
            portfolio_file_path = os.path.join(portfolio_folder_path, portfolio_file_name)
            operation = st.radio(
                'Selecione o tipo de operação:',
                ('Compra', 'Venda'))

            if operation == 'Compra':
                # Inserir novo registro em portfolio_file_path
                st.subheader('Insira os dados da operação de compra:')
                ticker_input = st.text_input("Informe o ticker do ativo comprado: ")
                order_qty_input = st.text_input('Informe a quantidade de ações:')
                cost_input = st.text_input('Informe o preço pago por ação:')

                if ticker_input and order_qty_input and cost_input:
                    ticker = str(ticker_input)

                    order_qty = float(order_qty_input)
                    cost = float(cost_input)
                    total_value = order_qty * cost
                
                if st.button('Enviar'):
                    # Lendo o arquivo JSON existente
                    with open(portfolio_file_path, 'r') as f:
                        data = json.load(f)
                    
                    # Verificando se o ticker já existe no JSON
                    ticker_exists = False
                    for item in data:
                        if item['Ticker'] == ticker + '.SA':
                            item['Quantidade'] += order_qty
                            item['Custo Total'] += total_value
                            # item['Custo Médio'] = item['Custo Total'] / item['Quantidade']
                            ticker_exists = True
                            break
                    
                    # Se o ticker não existir, adiciona um novo registro aos dados existentes
                    if not ticker_exists:
                        data.append({
                            'Ticker': ticker_input + '.SA',
                            'Quantidade': order_qty,
                            'Custo Total': total_value,
                            # 'Custo Médio': cost,                  
                        })
                    
                    # Escrevendo o arquivo JSON com todos os registros digitados
                    with open(portfolio_file_path, 'w') as f:
                        json.dump(data, f, indent=4)
                        st.write('Operação de compra registrada com sucesso.')

            elif operation == 'Venda':
                # Inserir novo registro em portfolio_file_path
                st.subheader('Insira os dados da operação de venda:')
                ticker_input = st.text_input("Informe o ticker do ativo vendido: ")
                order_qty_input = st.text_input('Informe a quantidade de ações:')

                if ticker_input and order_qty_input:
                    ticker = str(ticker_input)
                    order_qty = float(order_qty_input)

                if st.button('Enviar'):
                    # Lendo o arquivo JSON existente
                    with open(portfolio_file_path, 'r') as f:
                        data = json.load(f)
                    
                    for d in data:
                        if d['Ticker'] == ticker + '.SA':
                            d['Quantidade'] -= order_qty
                            # d['Custo Total'] -= d['Custo Médio'] * order_qty
                    
                    with open(portfolio_file_path, 'w') as f:
                        json.dump(data, f)

                    with open(portfolio_file_path, 'r') as f:
                        data = json.load(f)
                        
                    # Cria uma cópia do dicionário original
                    data_copy = data.copy()
                        
                    for item in data_copy:
                        if item['Quantidade'] <= 0:
                        # Remove o registro zerado
                            data.remove(item)

                    with open(portfolio_file_path, 'w') as f:
                        json.dump(data, f, indent=4)
                        st.write('Operação de venda registrada com sucesso.')
    if cic_search:
        new_op(cic_search)
client_search()

st.write("")
st.subheader("Visualização do Portfólio")
portfolio_search = st.text_input("Informe o código de identificação do cliente para exibir o portfolio")
portfolio_folder_path = "clients_portfolios"
portfolio_file_name = portfolio_search + '_portfolio.json'
portfolio_file_path = os.path.join(portfolio_folder_path, portfolio_file_name)

# Inicialize df como um DataFrame vazio
df_view = pd.DataFrame([])
df_pie = pd.DataFrame([])

if portfolio_search:
    portfolio_file_name = portfolio_search + '_portfolio.json'
    portfolio_file_path = os.path.join(portfolio_folder_path, portfolio_file_name)

    if os.path.exists(portfolio_file_path):
        # Carregando o JSON em um dataframe
        df = pd.read_json(portfolio_file_path)

    # definir função que coleta o preço atual a partir do ticker
    def get_price(ticker):
        ticker_yf = yf.Ticker(ticker)
        inf = ticker_yf.info
        try:
            current_price = float(inf['currentPrice'])
        except KeyError:
            history = ticker_yf.history(period="1d")
            current_price = history['Close'].iloc[-1]
        return current_price

    df['Preço'] = df['Ticker'].apply(get_price)

    # remover linhas com valores nulos (tickers inválidos)
    df = df.dropna()

    # adicionar coluna Valor Total multiplicando Quantidade por Preço
    df['Valor Total'] = df.apply(lambda row: row['Quantidade'] * row['Preço'], axis=1)

    # adicionar coluna Custo Unitário multiplicando Quantidade por Custo Unitário
    df['Custo Unitário'] = df.apply(lambda row: row['Custo Total'] / row['Quantidade'], axis=1)

    # Seleção de ordem
    order = st.radio('Selecione a ordem das colunas:', ['% Carteira', 'Lucro/Prejuízo'])
    
    # adicionar coluna Lucro/Prejuízo
    df['Lucro/Prejuízo'] = df.apply(lambda row: row['Valor Total'] / row['Custo Total'], axis=1)
    df['Lucro/Prejuízo'] = ((df['Lucro/Prejuízo'] - 1) * 100).round(2)
    if order == 'Lucro/Prejuízo':
        df = df.sort_values('Lucro/Prejuízo', ascending=False)
    df['Lucro/Prejuízo'] = df['Lucro/Prejuízo'].astype(str) + '%'

    # adicionar coluna Percentual
    df['% Carteira'] = ((df['Valor Total'] / df['Valor Total'].sum()) * 100).round(2)
    if order == '% Carteira':
        df = df.sort_values('% Carteira', ascending=False)
    df['% Carteira'] = df['% Carteira'].astype(str) + '%'

    df['Custo Unitário'] = df['Custo Unitário'].astype(float)
    df['Custo Unitário'] = [f'R$ {x:.2f}' for x in df['Custo Unitário']]

    df['Preço'] = df['Preço'].astype(float)
    df['Preço'] = [f'R$ {x:.2f}' for x in df['Preço']]

    df['Custo Total'] = df['Custo Total'].astype(float)
    df['Custo Total'] = [f'R$ {x:.2f}' for x in df['Custo Total']]

    df['Valor Total (R$)'] = df.apply(lambda row: row['Quantidade'] * row['Preço'], axis=1)

    df['Valor Total'] = df['Valor Total'].astype(float)
    df['Valor Total (R$)'] = df['Valor Total']
    total_geral = df['Valor Total'].sum()
    df['Valor Total (R$)'] = [f'R$ {x:.2f}' for x in df['Valor Total']]

    # Selecionar a ordem desejada das colunas
    column_order_view = ['Ticker', 'Quantidade', 'Custo Unitário', 'Custo Total', 'Preço', 'Valor Total (R$)', 'Lucro/Prejuízo', '% Carteira']
    column_pie = ['Ticker', 'Quantidade', 'Custo Unitário', 'Custo Total', 'Preço', 'Valor Total', 'Lucro/Prejuízo', '% Carteira']

    # Reordenar as colunas do DataFrame
    df_view = df[column_order_view]
    df_pie = df[column_pie]

# Converter o dataframe em HTML e remover a primeira coluna numerada
html = df_view.to_html(index=False)

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

st.write("")

if portfolio_search:
    total_geral = f'R$ {total_geral:.2f}'
    st.write(f'Valor total da carteira:', total_geral)

# Plotar um gráfico de pizza
if not df_pie.empty:
    labels = df['Ticker']
    values = df['Valor Total']
    plt.figure(figsize=(9, 9))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    # Definir a cor de fundo como azul
    plt.gca().patch.set_facecolor('blue')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(plt)