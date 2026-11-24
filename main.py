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

if menu == "Pedidos":
    pedidos = db.listar_pedidos()
    df_pedidos = pd.DataFrame(pedidos, columns=["ID", "CLIENTE", "VALOR", "STATUS", "PAGAMENTO", "TEMPO (min)"])

    total_pedidos = len(df_pedidos)
    em_andamento = len(df_pedidos[df_pedidos["STATUS"].isin(["Recebido", "Preparando"])]) if not df_pedidos.empty else 0
    concluidos = len(df_pedidos[df_pedidos["STATUS"] == "Concluido"]) if not df_pedidos.empty else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Pedidos", total_pedidos)
    col2.metric("Em Andamento", em_andamento)
    col3.metric("Concluídos", concluidos)

    st.markdown("---")

    with st.container(border=True):
        st.subheader("CADASTRAR NOVO PEDIDO")
        with st.form("form_pedidos", clear_on_submit=True):
            c1, c2 = st.columns(2)
            cliente = c1.text_input("Nome do cliente")
            forma_pagamento = c2.selectbox("Forma de pagamento", ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinherio"])

            c3, c4 = st.columns(2)
            valor_total = c3.number_input("Valor Total R$", min_value=0.0, step=5.0, format="%.2f")
            status = c4.selectbox("Status", ["Recebido", "Preparando", "Concluído"])



elif menu == "Entregadores":
    st.title("Entregadores")
    st.info("Próximo passo. . . ")

elif menu == "Entregas":
    st.title("Entregas")
    st.info("Em breve. . . ")

elif menu == "Financeiro":
    st.title("Financeiro")
    st.info("Em breve. . . ")