import streamlit as st
import acessosAva as aa

st.set_page_config(
    page_title="Dashboard NEAD",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("NEAD")

pagina = st.sidebar.selectbox(
    "Selecione o dashboard",
    [
        "Acessos - TEC.PRESENCIAL",
    ]
)

if pagina == "Acessos - TEC.PRESENCIAL":
    aa.acessoAva()