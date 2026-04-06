import streamlit as st
import google.generativeai as genai

# Configuração visual
st.set_page_config(page_title="O Aprendiz - Técnico Administrativo", page_icon="💼")

st.title("💼 O Aprendiz: Edição Administrativa")
st.subheader("Simulador de Tomada de Decisão")

# Barra lateral
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/pt/2/2b/O_Aprendiz_Logo.png", width=150)
    st.write("### Configuração")
    # O .strip() aqui vai limpar qualquer espaço invisível
    api_input = st.text_input("Insira sua Gemini API Key:", type="password")
    api_key = api_input.strip() 

SYSTEM_PROMPT = """
Você é o mestre de um RPG educacional chamado "O Aprendiz Administrativo", baseado no Roberto Justus.
Seja formal, exigente e apresente desafios técnicos de Técnico Administrativo (RH, Financeiro, Logística).
Sempre dê 3 opções (A, B e C).
Se o aluno errar 3 vezes, diga: "VOCÊ ESTÁ DEMITIDO!".
"""

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

        if "chat" not in st.session_state:
            st.session_state.chat = model.start_chat(history=[])
            response = st.session_state.chat.send_message("Comece o jogo como Roberto Justus com um desafio de RH.")
            st.session_state.messages = [{"role": "assistant", "content": response.text}]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Sua decisão?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # Aqui ele vai nos mostrar o erro real!
        st.error(f"Ocorreu um erro: {e}")
else:
    st.warning("⚠️ Cole a chave API na esquerda para começar.")
