import streamlit as st 
import requests
import os
from pymongo import MongoClient


# Obtém o nome do host do FastAPI a partir da variável de ambiente ou usa 'fastapi' por padrão
fastapi_host = os.getenv('FASTAPI_HOST', 'fastapi')

# Conecta ao MongoDB
mongo_client = MongoClient(os.getenv("MONGO_URI", "mongodb://mongodb:27017/"))
db = mongo_client["local"]
feedback_collection = db["feedback"]


def submit_comment(comment, rating):
    response = requests.post(f"http://{fastapi_host}:8000/feedback/", json={"comment": comment, "rating": rating})
    print("Status Code:", response.status_code)  # Exibe status
    print("Response Content:", response.text)  # Exibe o conteúdo bruto da resposta
    
    try:
        feedback = response.json()
    except requests.exceptions.JSONDecodeError:
        st.error("Erro ao processar resposta do servidor. Verifique se FastAPI está funcionando corretamente.")
        return

    status_color = "green" if feedback['status'] == 'aprovado' else "red"
    
    st.write(f"**Você comentou:** {comment}")
    st.write(f"**Avaliação:** {rating} estrelas")
    st.write(f"**Feedback:** {feedback['descricao']}")
    st.markdown(f"**Status:** <span style='color:{status_color}'>{feedback['status']}</span>", unsafe_allow_html=True)


def display_feedback():
    st.subheader("Feedbacks Salvos")
    feedbacks = feedback_collection.find()
    
    for feedback in feedbacks:
        st.write(f"**ID:** {feedback['_id']}")
        st.write(f"**Comentário:** {feedback['comment']}")
        st.write(f"**Avaliação:** {feedback['rating']} estrelas")
        st.write(f"**Análise de sentimento:** {feedback.get('descricao')}")
        st.write(f"**Status:** {feedback.get('status', 'Não disponível')}")
        st.write("---")


st.title("Input de Comentários - Análise de Sentimentos")

tab1, tab2 = st.tabs(["Enviar Comentário", "Ver Feedbacks"])

with tab1:
    comment = st.text_input("Escreva seu comentário aqui:")
    rating = st.slider("Avaliação (1 a 5 estrelas):", 1, 5, 3)
    if st.button("Enviar"):
        submit_comment(comment, rating)

with tab2:
    display_feedback()