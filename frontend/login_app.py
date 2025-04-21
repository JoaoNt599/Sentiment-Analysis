import streamlit as st 
import requests


API_URL = "http://fastapi:8000"


def login():
    st.title("Login")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        # Envia para rota /login da API
        response = requests.post(
            f"{API_URL}/login",
            json={"username": username, "password": password}
        )

        if response.status_code == 200:
            access_token = response.json().get("access_token")

            # Salva o token no estado da sessão
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["token"] = access_token

            st.success("Login bem-sucedido")

            # Redireciona após login (opcional)
            st.markdown(
                """
                <meta http-equiv="refresh" content="1; url=http://localhost:8501/" />
                """,
                unsafe_allow_html=True,
            )
        else:
            st.error("Usuário ou senha inválidos")


def main():
    # Se já está logado
    if st.session_state.get("logged_in"):
        st.success(f"Você está logado como {st.session_state.get('username')}")
        st.write("Token JWT:", st.session_state.get("token"))
    else:
        login()


if __name__ == "__main__":
    main()