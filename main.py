import streamlit as st

st.title("Teste do sistema!")

st.write("Se você vê isso, é porque ta tudo funcionando bem")

if st.button("Teste de interatividade"):
    st.success("Tudo certo! O sistema está respondendo aos cliques")