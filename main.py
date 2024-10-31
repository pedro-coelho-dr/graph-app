import streamlit as st
from pages import test_page as tp
# Dicionário de páginas com as referências
pages = {
    "Página 1": tp,
}

# Menu lateral
st.sidebar.title("Menu")
page = st.sidebar.selectbox("Selecione a página", options=list(pages.keys()))

# Carregar a página selecionada
selected_page = pages[page]
selected_page.app()
