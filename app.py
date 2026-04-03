import streamlit as st
import google.generativeai as genai

# Configuração visual da página
st.set_page_config(page_title="O Aprendiz - Técnico Administrativo", page_icon="💼")

# CSS para deixar o visual mais limpo
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #1e1e1e; color: white; font-weight: bold; }
    .stTextInput>div>div>input { border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💼 O Aprendiz: Edição Administrativa")
st.subheader("Simulador de Tomada de Decisão")

# Barra lateral para colocar a chave que você pegou
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/pt/2/2b/O_Aprendiz_Logo.png", width=150)
    st.markdown("---")
    st.write("### Configuração")
    api_key = st.text_input("Insira sua Gemini API Key:", type="password")
    st.info("Professor, insira sua chave do Google para ativar o 'Roberto Justus'.")

# O "Cérebro" do Jogo - Instruções do Justus
SYSTEM_PROMPT = """
Você é o mestre de um RPG educacional chamado "O Aprendiz Administrativo", baseado no Roberto Justus.
Seu objetivo é avaliar alunos de um curso de Técnico Administrativo.
Seja formal, exigente e foque em eficiência e resultados.
A cada rodada, apresente um desafio técnico real e 3 opções (A, B e C).
Sempre use termos técnicos (KPIs, SWOT, Fluxo de Caixa, CLT).
Regra: Se o aluno errar 3 vezes, diga: "VOCÊ ESTÁ DEMITIDO!".
Se ele acertar 5, ele é o "Novo Contratado".
"""

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

        if "chat" not in st.session_state:
            st.session_state.chat = model.start_chat(history=[])
            # Mensagem inicial do jogo
            response = st.session_state.chat.send_message("Apresente-se como CEO e comece com o primeiro desafio de RH.")
            st.session_state.messages = [{"role": "assistant", "content": response.text}]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Qual é a sua decisão?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Erro na Chave de API: Verifique se copiou corretamente.")
else:
    st.warning("⚠️ Aguardando a API Key para começar a sala de reunião.")
