import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="O Aprendiz - Técnico", page_icon="💼")
st.title("💼 O Aprendiz: Edição Administrativa")

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/pt/2/2b/O_Aprendiz_Logo.png", width=150)
    st.write("---")
    api_key = st.text_input("Insira sua Gemini API Key:", type="password").strip()

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Chamada direta e simples
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if "chat" not in st.session_state:
            st.session_state.chat = model.start_chat(history=[])
            instrucao = "Você é o Roberto Justus. Se apresente formalmente e mande o 1º desafio de RH para a turma de Técnico Administrativo."
            response = st.session_state.chat.send_message(instrucao)
            st.session_state.messages = [{"role": "assistant", "content": response.text}]

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        if prompt := st.chat_input("Sua resposta:"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            
            response = st.session_state.chat.send_message(prompt)
            with st.chat_message("assistant"): st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Erro ao conectar com o Google. Verifique se a chave está correta. (Detalhe: {e})")
else:
    st.info("Aguardando a chave API para iniciar a reunião...")
