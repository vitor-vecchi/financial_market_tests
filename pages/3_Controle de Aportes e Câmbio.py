import pandas as pd
import json
import streamlit as st
import os

st.set_page_config(
    page_title="Controle de Aportes e Câmbio",
    page_icon="💰",
)

st.image('logo.png', caption=None, width=595, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
st.markdown("# Controle de Aportes e Câmbio")

# Inserir novo registro em TDAmeritrade.json
def new_op():
    st.subheader('Insira os dados da nova operação:')
    op_date_input = st.date_input('Informe a data da operação de câmbio:')
    aporte_input = st.text_input('Informe o valor do aporte em reais (R$)')
    net_dollars_input = st.text_input('Informe a quantia líquida em dólares (US$):')

    # Nome da pasta e arquivo JSON
    folder_path = "operations"
    file_name = "exchange_op.json"

    # Caminho completo do arquivo JSON
    file_path = os.path.join(folder_path, file_name)
    
    if op_date_input and aporte_input and net_dollars_input:
        op_date = str(op_date_input)
        aporte = float(aporte_input)
        net_dollars = float(net_dollars_input)
        op_ex_rate = aporte / net_dollars
    
    if st.button('Enviar'):


        # Lendo o arquivo JSON existente
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Adicionando o novo registro ao final do objeto data
        data.append({
            'Data': op_date, 
            'Valor': aporte, 
            'Dólares': net_dollars, 
            'Câmbio':  op_ex_rate
        })
            
        # Escrevendo o arquivo JSON com todos os registros digitados
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
            
        st.write('Dados adicionados com sucesso!')

    # Carregando o JSON em um dataframe
    st.write('\n')
    st.write('Selecione para visualizar o histórico das operações:')
    if st.button('Carregar dados'):
        df = pd.read_json(file_path)

        # Soma todos os valores da coluna "Valor" e "Dólares"
        df['Valor'] = df['Valor'].astype(float)
        total_reais = df['Valor'].sum()
        df['Valor'] = [f'R$ {x:.2f}' for x in df['Valor']]

        df['Dólares'] = df['Dólares'].astype(float)
        total_dollar = df['Dólares'].sum()
        df['Dólares'] = [f'US$ {x:.2f}' for x in df['Dólares']]

        df['Câmbio'] = df['Câmbio'].astype(float)
        df['Câmbio'] = [f'R$ {x:.2f}' for x in df['Câmbio']]

        avg_ex_rate = (total_reais / total_dollar).astype(float)

        # Imprime os resultados
        st.write(f"Total em reais: R$ {total_reais:.2f}")
        st.write(f"Total em dólares: R$ {total_dollar:.2f}")
        st.write(f"Taxa média de câmbio: R$ {avg_ex_rate:.2f}")

        # Converter o dataframe em HTML e remover a primeira coluna numerada
        html = df.to_html(index=False)

        # Exibir o HTML no Streamlit
        st.markdown(html, unsafe_allow_html=True)
new_op()