import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime
from datetime import timedelta
from datetime import date
import streamlit as st

def main():
    st.image('logo.png', caption=None, width=595, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    aplicacao = st.selectbox("Selecione a aplicação", ['Página Principal', 'Gestão de Riscos'])
    if aplicacao == 'Página Principal':
        st.title('Gestão de Riscos')
        st.markdown('Este aplicativo foi desenvolvido com a finalidade de facilitar a gestão de riscos para o mercado financeiro.')
    
    def beta():
        start_date = st.date_input("Selecione a data inicial: ")
        end_date = st.date_input("Selecione a data final: ")
        bench_name = "^BVSP"
        asset_name = st.text_input("Digite o ticker do ativo: ") + ".SA"
        if start_date and end_date and asset_name:
            df = yf.download([asset_name, bench_name], start = start_date, end = end_date)["Adj Close"]
            df.columns=['Asset','Benchmark'];
            df.dropna(inplace=True)
    
            df["% Benchmark"] = df["Benchmark"].pct_change()
            df["% Asset"] = df["Asset"].pct_change()
            df = df[1:]
    
            def calc_beta():
                beta = df["% Asset"].cov(df["% Benchmark"]) / df["% Benchmark"].var()
                if st.button('Calcular beta'):
                    st.write(beta)
            calc_beta()
    if aplicacao == 'Gestão de Riscos':
        beta()
main()
