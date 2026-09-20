import json
import os
import pandas as pd
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

# ---------------------------------------------------------
# 2. CARREGAMENTO E OBTENÇÃO DA API KEY (CRÍTICO)
# ---------------------------------------------------------
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
# 3. CARREGAMENTO SEGURO DOS DADOS (CSV e JSON)
# ---------------------------------------------------------
def carregar_dados():
    def buscar_caminho(nome):
        if os.path.exists(nome):
            return nome
        elif os.path.exists(f"data/{nome}"):
            return f"data/{nome}"
        return None

    perfil = "Não informado"
    produtos = "Não informados"
    transacoes = "Sem histórico de transações"
    atendimentos = "Sem histórico de atendimentos"

    p = buscar_caminho("perfil_investidor.json")
    if p:
        with open(p, "r", encoding="utf-8") as f:
            perfil = f.read()

    p = buscar_caminho("produtos_financeiros.json")
    if p:
        with open(p, "r", encoding="utf-8") as f:
            produtos = f.read()

    p = buscar_caminho("transacoes.csv")
    if p:
        df = pd.read_csv(p)
        transacoes = df.to_string(index=False)

    p = buscar_caminho("historico_atendimento.csv")
    if p:
        df = pd.read_csv(p)
        atendimentos = df.to_string(index=False)

    return perfil, produtos, transacoes, atendimentos

perfil_raw, produtos_raw, transacoes_raw, atendimentos_raw = carregar_dados()

# ---------------------------------------------------------
# 4. PERSONALIDADE E PROMPT COMPACTO
# ---------------------------------------------------------
PROMPT_SISTEMA = f"""
Você é o "ReEduca Finanças", um agente de IA especialista em consultoria e educação financeira no Brasil.

DADOS DO CLIENTE E DO SISTEMA:
- PERFIL DO CLIENTE:
{perfil_raw}

- PRODUTOS FINANCEIROS:
{produtos_raw}

- TRANSAÇÕES REGISTRADAS:
{transacoes_raw}

- HISTÓRICO DE ATENDIMENTOS:
{atendimentos_raw}

DIRETRIZES:
1. Responda com base nos dados do cliente acima (analise gastos, transações, perfil e metas quando solicitado).
2. Se o usuário perguntar sobre os gastos do João ou maiores despesas, analise a lista de transações e detalhe os valores.
3. Se a pergunta for totalmente fora do tema de finanças (ex: receita, clima, esportes), responda: "Como assistente de educação financeira, meu foco é ajudar na organização do seu orçamento e investimentos. Como posso te ajudar com suas finanças hoje?"
"""

# ---------------------------------------------------------
# 5. INTERFACE E CHAT
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
            with st.spinner("Analisando dados..."):
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
                    str_erro = str(erro)
                    if "429" in str_erro or "RESOURCE_EXHAUSTED" in str_erro:
                        st.warning("⏱️ Limite de requisições por minuto atingido no plano gratuito. Por favor, aguarde cerca de 30 a 40 segundos e tente novamente.")
                    else:
                        st.error(f"Erro na comunicação com a API: {erro}")
else:
    st.info("👈 Para começar a conversa, informe sua chave de API na barra lateral à esquerda.")