import yfinance as yf
import streamlit as st
import pandas as pd
import json
import locale

# Defina a localização para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR')

def process_json_data(json_file):
    # Inicialize o arquivo JSON com uma lista vazia se ele estiver vazio
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    # Percorre cada entrada no JSON
    for entry in data:
        codigo = entry.get("Código")
        acao = entry.get("Ação")
        if codigo is not None:
            # Faça algo com o código, por exemplo, exiba-o
            st.write(codigo)
        else:
            # Lida com o caso em que "Código" não está presente na entrada
            st.write("Chave 'Código' não encontrada na entrada")

        ticker = str(codigo) + ".SA"
        if ticker:

            ticker_yf = yf.Ticker(ticker)

            # carrega e transforma as informações, o demonstrativo de resultado do exercício e o balanço patrimonial em variáveis
            inf = ticker_yf.info
            inc_sta = ticker_yf.income_stmt
            bs = ticker_yf.balance_sheet
            qbs = ticker_yf.quarterly_balance_sheet

            # st.write(qbs)
            # st.write(inf)
            # st.write(inc_sta)   

            # carrega e exibe o preço atual; atribui o último fechamento à variável historical_price
            historical_price = ticker_yf.history(period="1d")
            current_price = float(inf['currentPrice'])
            st.write("Preço Atual:", current_price)
        
            stockholders_equity = qbs.loc['Stockholders Equity', '2023-03-31']
            total_debt = qbs.get('Total Debt', 0)
            st.write("Patrimônio Líquido do Acionista:", stockholders_equity)
            st.write("Dívida Total:", total_debt)

            try:
                ebitda = inc_sta.loc['EBITDA']
            except KeyError:
                try:
                    ebitda_avg = float(inf['ebitda'])
                    formatted_ebitda_avg = locale.currency(ebitda_avg, grouping=True)
                    st.write(f"EBITDA:", formatted_ebitda_avg)
                except KeyError:
                    try:
                        ebitda = inc_sta.loc['Pretax Income']
                        ebitda_avg = ebitda.mean()
                        formatted_ebitda_avg = locale.currency(ebitda_avg, grouping=True)
                        st.write(f"EBITDA:", formatted_ebitda_avg)
                    except KeyError:
                        ebitda_avg = 0
                        st.write(f"EBITDA:", ebitda_avg)
            else:
                # Calculate EBITDA average for the last avaliable 4 years
                ebitda_avg = ebitda.mean()
                formatted_ebitda_avg = locale.currency(ebitda_avg, grouping=True)
                st.write(f"EBITDA Médio (Últimos 4 anos):", formatted_ebitda_avg)

            try:
                ebit = inc_sta.loc['EBIT']
            except KeyError:
                try:
                    ebit_avg = float(inf['ebit'])
                    formatted_ebit_avg = locale.currency(ebitda_avg, grouping=True)
                    st.write(f"EBIT:", formatted_ebit_avg)
                except:
                    ebit_avg = 0
                    st.write(f"EBIT:", ebit_avg)
            else:
                # Calculate EBITDA average for the last avaliable 4 years
                ebit_avg = ebit.mean()
                formatted_ebit_avg = locale.currency(ebit_avg, grouping=True)
                st.write(f"EBIT Médio (Últimos 4 anos):", formatted_ebit_avg)

            # display financials using pandas to loc 'EBIT'
            net_income = inc_sta.loc['Net Income Common Stockholders']
            # Calculate EBIT average for the last avaliable 4 years
            net_income_avg = net_income.mean()
            st.write(f"Lucro Líquido Médio nos últimos 4 anos:", net_income_avg)

            # Verifique se 'forwardEps' está presente nas informações
            if 'forwardEps' in inf and inf['forwardEps'] is not None:
                est_fwd_EPS = float(inf['forwardEps'])
                est_earnings_Yield = (est_fwd_EPS / current_price) * 100
                est_price_to_Earnings = (current_price / est_fwd_EPS)
                st.write("LPA Estimado - 12 m:", est_fwd_EPS)
                st.write("PE Estimado:", est_price_to_Earnings)
                st.write("Earnings Yield Estimado:", "%.3f" % est_earnings_Yield, "%")
            else:
                est_fwd_EPS = float(inf['trailingEps'])
                est_earnings_Yield = (est_fwd_EPS / current_price) * 100
                est_price_to_Earnings = (current_price / est_fwd_EPS)
                st.write("LPA Estimado - 12 m:", est_fwd_EPS)
                st.write("PE Estimado:", est_price_to_Earnings)
                st.write("Earnings Yield Estimado:", "%.3f" % est_earnings_Yield, "%")
            
            # Show 'sharesOutstanding' from info
            shares_Outs = float((inf['sharesOutstanding']))
            earnings_yield_Ebit = ((ebit_avg / (shares_Outs * current_price)) * 100)
            st.write("Earnings Yield do EBIT:", "%.3f" % earnings_yield_Ebit,"%")

            # display balance sheet using pandas to iloc 'Total Assets'
            total_Assets = qbs.loc['Total Assets', '2023-03-31']

            total_Current_Liabilities = qbs.loc['Total Liabilities Net Minority Interest', '2023-03-31']

            # Calcula o ROCE (retorno sobre o capital empregado)
            roce = ((ebit_avg / (total_Assets - total_Current_Liabilities)) * 100)
            net_assets = (total_Assets - total_Current_Liabilities)

            st.write("Retorno sobre o Capital Empregado", "%.3f" % roce,"%")
            st.write("Ativos Líquidos excl. Passivo Circulante:", net_assets)

            try:
                long_term_Debt = bs.loc['Long Term Debt', '2021-12-31']
            except KeyError:
                long_term_Debt = total_debt

            st.write("Dívida de Longo Prazo:", long_term_Debt)

            # Calcula o ROCE alternativo
            alt_roce = ((ebit_avg / (stockholders_equity - long_term_Debt)) * 100)
            net_equity = (stockholders_equity - long_term_Debt)
            st.write("Retorno sobre o Capital Empregado - Alternativo:", "%.3f" % alt_roce,"%")

            final_roce = (roce + alt_roce) / 2

            st.write("Patrimônio excl. Dívida de Longo Prazo:", net_equity)
            st.write("\n")
            st.write("\n")

            metrics = {
                'Código': codigo,
                'Ação': acao,
                'LPA estimado': est_fwd_EPS,
                'Earnings Yield - Net Income (Estimado)': est_earnings_Yield,
                'Earnings Yield EBIT': earnings_yield_Ebit,
                'ROCE': final_roce
            }

            # Adicione as métricas ao JSON
            entry.update(metrics)
            
        # Salve os dados atualizados no arquivo JSON
    with open('stock_fundamentals.json', "w") as f:
        json.dump(data, f, indent=4)    

# Chamada da função para processar o arquivo JSON
process_json_data('stock_data_test.json')

df = pd.read_json('stock_fundamentals.json')

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