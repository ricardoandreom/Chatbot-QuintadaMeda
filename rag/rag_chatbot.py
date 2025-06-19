from openai import OpenAI
import os
import streamlit as st
from config import api_key

def responder_com_rag(pergunta, retriever):
    docs = retriever.get_relevant_documents(pergunta)
    contexto = "\n".join(d.page_content for d in docs)

    prompt = f"""
    Usa o seguinte contexto para responder a pergunta do cliente. Responde de forma clara, educada e com base apenas na informação dada.

    Contexto:
    {contexto}

    Pergunta:
    {pergunta}

    Resposta:
    """

    #
    client = OpenAI(api_key=api_key)
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return resposta.choices[0].message.content.strip()
