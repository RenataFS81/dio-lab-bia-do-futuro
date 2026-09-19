# Código da Aplicação
import streamlit as st
from google import genai

# ---------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA STREAMLIT
# ---------------------------------------------------------
st.set_page_config(
    page_title="ReEduca Finanças",
    page_icon="💰",
    layout="centered"
)

st.title("💰 ReEduca Finanças")
st.subheader("Seu Agente de Consultoria e Planejamento Financeiro")
st.markdown("---")

# Carrega a chave dos Secrets ou da barra lateral
api_key = ""
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except (FileNotFoundError, KeyError, Exception):
    api_key = ""

if not api_key:
    with st.sidebar:
        st.header("⚙️ Configurações")
        api_key = st.text_input("Informe sua API Key do Gemini:", type="password")
        st.caption("Obtenha sua chave gratuitamente no Google AI Studio.")

# ---------------------------------------------------------
# 2. PERSONALIDADE E GUARDRAILS (System Prompt)
# ---------------------------------------------------------
PROMPT_SISTEMA = """
Você é o "ReEduca Finanças", um agente de IA especializado exclusivamente em consultoria e educação financeira no contexto brasileiro.

REGRAS RÍGIDAS DE ESCOPO:
1. Responda APENAS sobre finanças pessoais, orçamento, dívidas, investimentos, reserva de emergência e economia doméstica.
2. Se a pergunta for sobre qualquer outro assunto (ex: clima, tempo da natureza, esportes, receitas, fofocas, curiosidades gerais):
   - NÃO tente criar metáforas.
   - NÃO tente relacionar o assunto com finanças.
   - Responda EXATAMENTE: "Como assistente de educação financeira, meu foco é ajudar na organização do seu orçamento e investimentos. Como posso te ajudar com suas finanças hoje?"

DIRETRIZES CONSULTIVAS:
1. Mantenha um tom profissional, empático e objetivo.
2. Termine sempre sugerindo um próximo passo prático sobre o orçamento do usuário.
"""

# ---------------------------------------------------------
# 3. INTERFACE E LÓGICA DO CHAT
# ---------------------------------------------------------
if api_key:
    client = genai.Client(api_key=api_key)

    if "historico" not in st.session_state:
        st.session_state.historico = []

    for mensagem in st.session_state.historico:
        with st.chat_message(mensagem["papel"]):
            st.markdown(mensagem["conteudo"])

    if entrada_usuario := st.chat_input("Digite sua dúvida ou objetivo financeiro..."):
        st.session_state.historico.append({"papel": "user", "conteudo": entrada_usuario})
        with st.chat_message("user"):
            st.markdown(entrada_usuario)

        with st.chat_message("assistant"):
            with st.spinner("Analisando..."):
                try:
                    resposta = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=entrada_usuario,
                        config={'system_instruction': PROMPT_SISTEMA}
                    )
                    
                    texto_resposta = resposta.text
                    st.markdown(texto_resposta)
                    st.session_state.historico.append({"papel": "assistant", "conteudo": texto_resposta})

                except Exception as erro:
                    mensagem_erro = "Desculpe, estou enfrentando uma alta demanda de conexões no momento. Por favor, tente enviar sua mensagem novamente em alguns segundos!"
                    st.warning(mensagem_erro)
                    st.session_state.historico.append({"papel": "assistant", "conteudo": mensagem_erro})
else:
    st.info("👈 Para começar a conversa, informe sua chave de API na barra lateral à esquerda.")
## Estrutura Sugerida

```
src/
├── app.py              # Aplicação principal (Streamlit/Gradio)
├── agente.py           # Lógica do agente
├── config.py           # Configurações (API keys, etc.)
└── requirements.txt    # Dependências
```

## Exemplo de requirements.txt

```
streamlit
openai
python-dotenv
```

## Como Rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
streamlit run app.py
```
