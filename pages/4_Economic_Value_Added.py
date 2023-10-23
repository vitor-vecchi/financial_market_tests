import pandas as pd
import streamlit as st
import yfinance as yf
import json

def main():
    st.header("Calculadora do Economic Value Added (EVA)")
    
    # Solicite ao usuário o ticker da empresa
    ticker_empresa = st.text_input("Digite o Ticker da empresa na B3:")

    if ticker_empresa:  # Verifica se o campo de entrada não está vazio
        total_debt = calc(ticker_empresa)  # Armazena o total_debt retornado por calc

        if total_debt is not None:
            debts = debt_calculation(total_debt)  # Passa total_debt como argumento para debt_calculation

def calc(ticker_empresa):
    ticker_yf = yf.Ticker(ticker_empresa + ".SA")
    bs = ticker_yf.quarterly_balance_sheet
    stockholders_equity = bs.loc['Stockholders Equity', '2023-06-30']
    total_debt = bs.loc['Total Debt', '2023-06-30']

    if not pd.isna(stockholders_equity) and not pd.isna(total_debt):
        st.write(f"Ticker: {ticker_empresa}")
        st.write(f"Patrimônio Líquido: R${stockholders_equity / 10**9:.2f} bilhões")
        st.write(f"Dívida Total: R${total_debt / 10**9:.2f} bilhões")
        return total_debt  # Retorna o total_debt
    else:
        st.write(f"Dados não encontrados para o ticker: {ticker_empresa}")
        return None  # Retorna None se os dados não forem encontrados

def debt_calculation(total_debt):
    st.title("Calculadora de Média Ponderada de Dívidas")

    debts = []
    checkbox_counter = 1
    divida_counter = 100

    if st.checkbox("Adicionar Dívida", key=checkbox_counter):
        debt_name_input = st.text_input("Nome da Dívida")
        rate_name_input = st.selectbox("Indexador da dívida", ["CDI", "IPCA+", "TJLP", "Prefixada", "SELIC"])
        rate_value_input = st.number_input("Taxa:")
        weight_value_input = st.number_input("Representatividade (peso):")
        st.write(f"A dívida total a ser calculada é", total_debt)
        st.write('')
        
        checkbox_counter += 1
        
        # segregation = st.checkbox("Segregar essa dívida", key=divida_counter)

        if debt_name_input and rate_name_input and rate_value_input and weight_value_input:
            debt_name = str(debt_name_input)
            rate_name= str(rate_name_input)
            rate_value = float(rate_value_input)
            weight_value = float(weight_value_input)
 

        # if segregation:
            # segregation_name = st.text_input("Nome da Segregação")
            # segregation_weight = st.number_input("Representatividade (Peso) da Segregação")
            # rate_value /= segregation_weight  # Calcula o valor da taxa ponderada

        if st.button('Enviar'):
            # Lendo o arquivo JSON existente
            with open('eva.json', 'r') as f:
                data = json.load(f)
            
            # Adicionando o novo registro ao final do objeto data
            data.append({
                'Nome da dívida': debt_name,
                'Indexador da dívida': rate_name,
                'Taxa': rate_value,
                'Representatividade': weight_value
            })
        
            # Escrevendo o arquivo JSON com todos os registros digitados
            with open('eva.json', 'w') as f:
                json.dump(data, f, indent=4)

            st.write('Dados adicionados com sucesso!')

            df = pd.read_json('eva.json')
            # Converter o dataframe em HTML e remover a primeira coluna numerada
            html = df.to_html(index=False)

            # Exibir o HTML no Streamlit
            st.markdown(html, unsafe_allow_html=True)


    return debts

if __name__ == "__main__":
    main()
