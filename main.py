import streamlit as st
from app_pages import home, test_page

# Dicionário com as páginas que devem aparecer no menu
pages = {
    "Home": home,
    "Página de Teste": test_page,
}

# Menu lateral
st.sidebar.title("Menu")
page = st.sidebar.radio("Navegação", list(pages.keys()))

# Carregar a página selecionada
selected_page = pages[page]
selected_page.app()
