import streamlit as st
from rag.loader import load_documents_from_txt
from rag.retriever import create_retriever
from rag.rag_chatbot import responder_com_rag

st.set_page_config(page_title="Chatbot Quinta da Meda", layout="centered")
st.title("🤖 Chatbot - Quinta da Meda")

# Inicializa chatbot
@st.cache_resource
def setup_chatbot():
    docs = load_documents_from_txt()
    retriever = create_retriever(docs)
    return retriever

retriever = setup_chatbot()

# Inicializa histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe histórico de chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input do user
pergunta = st.chat_input("Faça a sua pergunta sobre o alojamento:")

if pergunta:
    # Guarda pergunta do user
    st.session_state.messages.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    # Obtém resposta do chatbot
    resposta = responder_com_rag(pergunta, retriever)

    # Guarda e mostra resposta do chatbot
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.markdown(resposta)

# Botão para reset do histórico (opcional)
if st.button("🔁 Reset no chat"):
    st.session_state.messages = []
    st.experimental_rerun()
