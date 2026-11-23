import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mão na Massa", page_icon="🍝", layout="wide")

if "pedidos_temp" not in st.session_state:
    st.session_state.pedidos_temp = []

st.sidebar.title("🍝 Mão na Massa")
menu = st.sidebar.radio("Escolha a tela:", ["Pedidos", "Entregadores", "Entregas", "Financeiro"])

if menu == "Pedidos":
    st.title("Pedidos")

    with st.form("form_teste", clear_on_submit=True):
        cliente = st.text_input("Nome do Cliente")
        prato = st.text_input("Pedido (Ex: Lasanha)")
        valor = st.number_input("Valor do pedido", min_value=0.0, step=5.0)

        if cliente and prato:
            st.session_state.pedidos_temp.append({
                "Cliente": cliente,
                "Prato": prato,
                "Valor (R$)": valor,
            })
            st.success("Adicionado")

if menu == "Entregadores":
    st.title("Entregadores")

if menu == "Entregas":
    st.title("Entregas")

if menu == "Financeiro":
    st.title("Financeiro")