import streamlit as st
import pandas as pd
import database as db

st.set_page_config(page_title="Mão na Massa", page_icon="images/logo-da-empresa-icone.png", layout="wide")

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
    concluidos = len(df_pedidos[df_pedidos["STATUS"] == "Concluído"]) if not df_pedidos.empty else 0

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

            tempo_prep = st.number_input("Tempo de preparação (min)", min_value=5, max_value=180, value=30, step=5)

            _, col_btn = st.columns([4, 1])
            submitted = col_btn.form_submit_button("Cadastrar Pedido", use_container_width=True)

            if submitted:
                if cliente and valor_total > 0:
                    db.inserir_pedido(cliente, forma_pagamento, valor_total, status, tempo_prep)
                    st.success("Pedido cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.warning("Preencha o nome do cliente e um valor maior que zero. ")

    st.subheader("PEDIDOS RECENTES")
    if not df_pedidos.empty:
        df_exibicao = df_pedidos[["ID", "CLIENTE", "VALOR", "STATUS"]].copy()
        df_exibicao["ID"] = df_exibicao["ID"].apply(lambda x: f"#{x}")
        df_exibicao["VALOR"] = df_exibicao["VALOR"].apply(lambda x: f"R$:{x:,.2f}".replace(".", ","))

        st.dataframe(df_exibicao, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum pedido cadastrado ainda.")

elif menu == "Entregadores":
    st.title("Entregadores")
    st.info("Próximo passo. . . ")

elif menu == "Entregas":
    st.title("Entregas")
    st.info("Em breve. . . ")

elif menu == "Financeiro":
    st.title("Financeiro")
    st.info("Em breve. . . ")


# st.logo("images/logo-da-empresa-icone.png")