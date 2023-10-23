import streamlit as st
import json
import os

st.set_page_config(
    page_title="Página Principal",
    page_icon="📈",
)

st.image('logo.png', caption=None, width=595, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
st.markdown("# Página Principal")

st.write(
    """Este programa foi escrito em Python e visa facilitar o
    processo de planejamento financeiro, contempladas as etapas 
    de análise do perfil do investidor, a gestão financeira, 
    a gestão patrimonial, o planejamento sucessório, tributário, 
    previdenciário, a gestão de riscos, bem como a coleta de dados
    para a realização de todos os processos pertinentes."""
)
st.write("\n")

st.subheader("Cadastro de Clientes")
cic_new = st.text_input("Digite o código de identificação do cliente para incluir novo cadastro no banco de dados (Formato: CIC-NUM):")
name = st.text_input("Digite o nome do cliente:")


if st.button('Cadastrar novo cliente'):
    # Nome do arquivo JSON e caminho da pasta
    file_name = "clients.json"
    folder_path = "client_data"

    # Verifica se a pasta existe, caso contrário, cria-a
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Caminho completo do arquivo JSON
    file_path = os.path.join(folder_path, file_name)

    if cic_new and name:
        # Coleta informações do cliente
        client_info = {
            "Código de Identificação": cic_new,
            "Nome": name,
        }

    # Lê os dados existentes do arquivo JSON, se houver
    data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            data = json.load(json_file)

    # Adiciona as informações do cliente aos dados existentes
    data.append(client_info)

    # Escreve os dados atualizados no arquivo JSON
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
        st.write('Registro incluído com sucesso.')

col1, col2 = st.columns(2)

with col1:
    st.image('col1.png', caption=None, width=300, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

with col2:
    st.image('col2.png', caption=None, width=300, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
