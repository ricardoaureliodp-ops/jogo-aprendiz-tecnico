import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="O Aprendiz - Técnico", page_icon="💼")
st.title("💼 O Aprendiz: Edição Administrativa")

# Tenta pegar a chave do cofre secreto do Streamlit
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = None

# Se a chave estiver no cofre, esconde a caixa de senha e mostra uma mensagem de sucesso
if api_key:
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/pt/2/2b/O_Aprendiz_Logo.png", width=150)
        st.success("✅ Sessão conectada com sucesso!")
else:
    # Se não achar no cofre (segurança extra), pede na tela
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/pt/2/2b/O_Aprendiz_Logo.png", width=150)
        api_key = st.text_input("Insira sua Gemini API Key:", type="password").strip()

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        if "model_name" not in st.session_state:
            modelos_disponiveis = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            st.session_state.model_name = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in modelos_disponiveis else modelos_disponiveis[0]
        
        model = genai.GenerativeModel(st.session_state.model_name)
        
        if "chat" not in st.session_state:
            st.session_state.chat = model.start_chat(history=[])
            instrucao = "Você é o Roberto Justus. Se apresente e mande o 1º desafio de RH para a turma de Técnico Administrativo."
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
        st.error(f"Erro ao carregar o mestre: {e}")
else:
    st.info("Aguardando a conexão da sala de reunião...")
