import streamlit as st
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import locale

# Defina a localização para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR')

st.title('Análise Fundamentalista de Ações')
st.subheader('Indicadores relevantes')

market = st.selectbox("Selecione o mercado", ['Brasil 🇧🇷', 'Estados Unidos da América 🇺🇸'])

if market == 'Brasil 🇧🇷':
    stock = st.text_input('Informe o ticker da ação:', '') + '.SA'   

if market == 'Estados Unidos da América 🇺🇸':
    stock = st.text_input('Informe o ticker da ação:', '') 
    
def main(stock):
    global ticker_yf
    ticker_yf = yf.Ticker(stock)
    
    if st.button('Enviar'):
        def calc():
            inf = ticker_yf.info
            bs =  ticker_yf.balance_sheet
            qbs = ticker_yf.quarterly_balance_sheet

            current_price = float(inf['currentPrice'])
            formatted_current_price = locale.currency(current_price, grouping=True)
            st.write(f"Cotação atual:", formatted_current_price)
            
            try:
                long_term_debt_serie = bs.loc['Long Term Debt']
                long_term_debt = long_term_debt_serie.mean()
            except KeyError:
                total_debt = qbs.loc('Total Debt')
                long_term_debt = total_debt

            fin =  ticker_yf.income_stmt
            ebit = fin.loc['EBIT']
            ebit_avg = ebit.mean()
            st.write("EBIT Médio - últimos 4 anos:", ebit_avg)
            st.write("\n")

            shares_Outs = float((inf['sharesOutstanding']))
            est_fwd_EPS = float((inf['forwardEps']))
            est_earnings_Yield = (est_fwd_EPS / current_price) * 100
            earnings_yield_Ebit = ((ebit_avg / (shares_Outs * current_price)) * 100)
            est_price_to_Earnings = (current_price / est_fwd_EPS)

            st.write("Earnings Yield do EBIT:", "%.3f" % earnings_yield_Ebit + "%")
            st.write("LPA Estimado para 12 meses:", est_fwd_EPS)
            st.write("Earnings Yield Estimado:", "%.3f" % est_earnings_Yield + "%")
            st.write("PE Estimado:", "%.3f" % est_price_to_Earnings + "x")
            st.write("\n")

            total_assets_series = bs.loc['Total Assets']
            total_assets_avg = total_assets_series.mean()

            current_liabilities = bs.loc['Current Liabilities']
            current_liabilities_avg = current_liabilities.mean()

            roce = ((ebit_avg / (total_assets_avg - current_liabilities_avg)) * 100)

            net_assets_avg = (total_assets_avg - current_liabilities_avg)

            st.write("Retorno sobre o Capital Empregado:", "%.3f" % roce + "%")
            st.write("Ativos Líquidos excl. Passivo Circulante:", net_assets_avg)

            stockholders_equity_series = bs.loc['Stockholders Equity']
            stockholders_equity = stockholders_equity_series.mean()

            st.write("Patrimônio Líquido do Acionista:", stockholders_equity)

            st.write("Dívida de Longo Prazo:", long_term_debt)

            alt_roce_serie = ((ebit_avg / (stockholders_equity - long_term_debt)) * 100)
            alt_roce = float(alt_roce_serie)

            net_equity = (stockholders_equity - long_term_debt)
            st.write("Retorno sobre o Capital Empregado - Alternativo:", "%.3f" % alt_roce + "%")

            st.write("Patrimônio excl. Dívida de Longo Prazo:", net_equity)
        calc()
main(stock)