import streamlit as st 
import redis


# Configuração do Redis
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# Mock de usuário e senha
MOCK_USER = "admin"
MOCK_PASSWORD = "1234"

# Tempo da sessão
SESSION_TTL = 1800 # 30 minutos


def login():
    st.title("Login")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if username == MOCK_USER and password == MOCK_PASSWORD:
            session_key = f"session:{username}"
            created = r.setex(session_key, SESSION_TTL, "active")

            if created:
                st.success("Login bem-sucedido")
            else:
                st.error("Falha ao criar sessão no Redis.")

            # r.setex(session_key, SESSION_TTL, "active")
            # st.success("Login bem-sucedido")

            # Redireciona após login
            st.markdown(
                """
                <meta http-equiv="refresh" content="1; url=http://localhost:8501/" />
                """,
                unsafe_allow_html=True,
            )
        else:
            st.error("Usuário ou senha inválidos.")
        

def main():
    login()


if __name__ == "__main__":
    main()