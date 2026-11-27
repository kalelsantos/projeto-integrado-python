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
            cliente = c1.text_input("Nome do cliente").title()
            forma_pagamento = c2.selectbox("Forma de pagamento", ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"])

            c3, c4 = st.columns(2)
            valor_total = c3.number_input("Valor Total R$", min_value=0.0, step=5.0, format="%.2f")
            status = c4.selectbox("Status", ["Recebido", "Preparando", "Concluído"])

            tempo_prep = st.number_input("Tempo de preparação (min)", min_value=5, max_value=180, value=30, step=5)
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            _, col_btn = st.columns([2, 1])
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
        st.info("Nenhum pedido cadastrado até agora.")


elif menu == "Entregadores":
    entregadores = db.listar_entregadores()
    df_entregadores = pd.DataFrame(entregadores, columns=["ID", "NOME", "VEÍCULO", "TELEFONE", "STATUS", "ENTREGAS", "AVALIAÇÃO"])

    total_cadastrados = len(df_entregadores)
    disponiveis = len(df_entregadores[df_entregadores["STATUS"] == "Disponível"]) if not df_entregadores.empty else 0
    indisponiveis = len(df_entregadores[df_entregadores["STATUS"] != "Disponível"]) if not df_entregadores.empty else 0
    avaliacao_media = df_entregadores["AVALIAÇÃO"].mean() if not df_entregadores.empty else 5.0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cadastrados", total_cadastrados)
    col2.metric("Disponíveis", disponiveis)
    col3.metric("Indisponíveis", indisponiveis)
    col4.metric("Avaliação Média", f"{avaliacao_media:.2f}")

    st.markdown("---")

    with st.container(border=True):
        st.subheader("CADASTRAR NOVO ENTREGADOR")
        with st.form("form_entregadores", clear_on_submit=True):
            col_esq, col_dir = st.columns(2)
            with col_esq:
                nome_motoboy = st.text_input("Nome do Motoboy").title()
                telefone_motoboy = st.text_input("Telefone")

            with col_dir:
                veiculo_motoboy = st.selectbox("Tipo de Veículo", ["Carro", "Motocicleta", "Bicicleta"])
                status_motoboy = st.selectbox("Status", ["Disponível", "Em Rota", "Indisponível"])
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True) 
                submitted = st.form_submit_button("Cadastrar Motoboy", use_container_width=True)

            if submitted:
                if nome_motoboy and telefone_motoboy.strip():
                    db.inserir_entregador(nome_motoboy.strip(), veiculo_motoboy, telefone_motoboy.strip(), status_motoboy)
                    st.success("Motoboy cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.warning("Preencha o nome e o telefone do motoboy. ")

    st.subheader("MOTOBOYS")
    if df_entregadores.empty:
        st.info("Nenhum entregador cadastrado ainda. ")
    else:
        df_entregadores["ID"] = "#" + df_entregadores["ID"].astype(str)
        df_entregadores["ENTREGAS"] = df_entregadores["ENTREGAS"].astype(str)
        df_entregadores["AVALIAÇÃO"] = df_entregadores["AVALIAÇÃO"].apply(lambda x: f"{x:.2f}")
        st.dataframe(df_entregadores, use_container_width=True, hide_index=True)


elif menu == "Entregas":
    entregas = db.listar_entregas()
    df_entregas = pd.DataFrame(entregas, columns=["ID", "PEDIDO", "MOTOBOY", "LOCALIZAÇÃO", "VALOR ENTREGA", "TEMPO ESTIMADO", "STATUS"])

    entregas_concluidas = len(df_entregas[df_entregas["STATUS"] == "Entregue"]) if not df_entregas.empty else 0

    tempo_medio = df_entregas["TEMPO ESTIMADO"].mean() if not df_entregas.empty else 0

    _, col1, _, col2, _ = st.columns([1.5, 2, 0.5, 2, 1])
    col1.metric("Entregas Concluídas", entregas_concluidas)
    col2.metric("Tempo Médio", f"{tempo_medio:.0f}")

    st.markdown("---")

    lista_pedidos = [p[0] for p in db.listar_pedidos() if p[3] != "Concluído"]
    lista_motoboys = [e[1] for e in db.listar_entregadores() if e[4] == "Disponível"]


    with st.container(border=True):
        st.subheader ("Distribuir Entrega")
        with st.form("form_entregas", clear_on_submit=True):
            col_esq, col_dir = st.columns(2)
            with col_esq:
                num_pedido = st.selectbox("Número do Pedido", lista_pedidos)
                valor_entrega = st.number_input("Valor de Entrega R$", min_value=0.0, step=1.0, format="%.2f")
                tempo_estimado = st.number_input("Tempo Estimado de Entrega (min)", min_value=5, max_value=180, value=20, step=5)
            with col_dir:
                endereco = st.text_input("Endereço de Entrega")
                entregador_resp = st.selectbox("Entregador Responsável", lista_motoboys)
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Distribuir Entrega", use_container_width=True)

        if submitted:
            if entregador_resp.strip() and endereco.strip() and num_pedido:
                db.inserir_entrega(num_pedido, entregador_resp, endereco.strip(), valor_entrega, tempo_estimado)
                st.success("Entrega registrada com sucesso!")
                st.rerun()
            else:
                st.warning("Preencha o endereço de entrega.")

    st.subheader("ACOMPANHAMENTO")
    if df_entregas.empty:
        st.info("Nenhuma entrega para acompanhar. ")
    else:
        df_exibicao = df_entregas.copy()
        df_exibicao["ID"] = df_exibicao["ID"].apply(lambda x: f"#{x}")
        df_exibicao["PEDIDO"] = df_exibicao["PEDIDO"].apply(lambda x: f"#{x}")
        df_exibicao["VALOR ENTREGA"] = df_exibicao["VALOR ENTREGA"].apply(lambda x: f"R$ {x:,.2f}".replace(".", ","))
        df_exibicao["TEMPO ESTIMADO"] = df_exibicao["TEMPO ESTIMADO"].apply(lambda x: f"{x} min")

        st.dataframe(df_exibicao, use_container_width=True, hide_index=True)


elif menu == "Financeiro":
    if "financeiro_liberado" not in st.session_state:
        st.session_state["financeiro_liberado"] = False
    if st.session_state["financeiro_liberado"] == False:
        with st.container(border=True):
            st.subheader("Acessar a aba financeiro")
            with st.form("form_senha", clear_on_submit=True):
                senha = st.text_input("Digite a senha para acessar a aba financeiro", type="password")

                submitted = st.form_submit_button("Entrar", use_container_width=True)

            if submitted:
                if senha == "123":
                    st.session_state["financeiro_liberado"] = True
                    st.session_state["mostrar_aviso"] = True
                    st.rerun()
                else:
                    st.error("Senha incorreta, tente novamente. ")
    else:
        st.title("FINANCEIRO")
        if st.session_state.get("mostrar_aviso"):
            st.toast("Acesso liberado com sucesso!")
            st.session_state["mostrar_aviso"] = False



















# st.logo("images/logo-da-empresa-icone.png")