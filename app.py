import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="O Aprendiz - Técnico Administrativo", page_icon="💼")

st.title("💼 O Aprendiz: Edição Administrativa")

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/pt/2/2b/O_Aprendiz_Logo.png", width=150)
    st.write("### Configuração")
    api_input = st.text_input("Insira sua Gemini API Key:", type="password")
    api_key = api_input.strip()

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Tiramos o "models/" da frente. Em muitos casos, isso resolve o erro 404 no Streamlit
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        instrucoes = (
            "Você é o Roberto Justus, mestre do RPG 'O Aprendiz Administrativo'. "
            "Seja formal, exigente e foque em eficiência. Teste alunos de um curso Técnico "
            "com desafios reais de RH, Finanças ou Logística. Dê 3 opções (A, B e C)."
        )

        if "chat" not in st.session_state:
            st.session_state.chat = model.start_chat(history=[])
            response = st.session_state.chat.send_message(instrucoes + " Comece se apresentando e mande o 1º desafio.")
            st.session_state.messages = [{"role": "assistant", "content": response.text}]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Qual sua decisão?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Ocorreu um erro de conexão: {e}")
else:
    st.info("Professor, cole a chave API na esquerda para abrir a sala de reunião.")
