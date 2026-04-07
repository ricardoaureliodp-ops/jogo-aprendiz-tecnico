import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="O Aprendiz - Técnico", page_icon="💼")
st.title("💼 O Aprendiz: Edição Administrativa")

# Puxa a chave do cofre secreto
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = None

if api_key:
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/pt/2/2b/O_Aprendiz_Logo.png", width=150)
        st.success("✅ Sessão conectada com sucesso!")
else:
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/pt/2/2b/O_Aprendiz_Logo.png", width=150)
        api_key = st.text_input("Insira sua Gemini API Key:", type="password").strip()

# Cache para não gastar cota lendo a lista toda hora
@st.cache_data
def pegar_modelos(chave):
    genai.configure(api_key=chave)
    return [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

if api_key:
    try:
        genai.configure(api_key=api_key)
        modelos = pegar_modelos(api_key)
        
        with st.sidebar:
            st.write("---")
            st.caption("🔧 Câmbio de Marcha (Modelos)")
            # Menu para você trocar o modelo caso o Google travar o atual
            modelo_escolhido = st.selectbox("Se o Justus travar, troque o cérebro aqui:", modelos)

        model = genai.GenerativeModel(modelo_escolhido)
        
        # Inicia o chat ou reinicia se você trocar de modelo
        if "chat" not in st.session_state or st.session_state.get("modelo_atual") != modelo_escolhido:
            st.session_state.chat = model.start_chat(history=[])
            st.session_state.modelo_atual = modelo_escolhido
            st.session_state.messages = []
            
            instrucao = "Você é o Roberto Justus. Se apresente e mande o 1º desafio de RH para a turma de Técnico Administrativo."
            response = st.session_state.chat.send_message(instrucao)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        if prompt := st.chat_input("Sua resposta:"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            
            response = st.session_state.chat.send_message(prompt)
            with st.chat_message("assistant"): st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Atenção: O Google bloqueou este cérebro temporariamente. (Detalhe: {e})")
        st.warning("👉 DICA DE MESTRE: Vá no menu esquerdo ali na barra e escolha OUTRO modelo (ex: models/gemini-1.5-flash) para continuar a aula na hora!")
else:
    st.info("Aguardando a conexão da sala de reunião...")
