import streamlit as st
import pandas as pd
import database as db

st.set_page_config(page_title="Mão na Massa", page_icon="🍝", layout="wide")

db.criar_tabelas()

st.sidebar.title('Mão na Massa')
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Menu",
    ["Pedidos", "Entregadores", "Entregas", "Financeiro"])

