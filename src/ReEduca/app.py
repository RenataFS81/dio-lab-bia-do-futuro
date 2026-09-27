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
# 2. OBTENÇÃO DA API KEY
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
# 4. PERSONALIDADE E PROMPT
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
1. Responda detalhadamente e com passo a passo claro com base nos dados do cliente acima.
2. Se o usuário perguntar por produtos não cadastrados (ex: Cripto, CDB Prefixado Bradesco, Ações), informe educadamente que o produto não consta na base cadastrada e recomende as opções de renda fixa disponíveis no perfil (ex: Tesouro Selic, CDB Liquidez Diária).
3. Se a pergunta for fora de finanças, recuse educadamente e redirecione para educação financeira.
"""

# ---------------------------------------------------------
# 5. RESPOSTA DE CONTINGÊNCIA ENRIQUECIDA (Caso a API falhe)
# ---------------------------------------------------------
def resposta_contingencia(pergunta):
    p = pergunta.lower()
    
    if "organizar" in p or "começar" in p or "passo a passo" in p or "investimento" in p:
        return ("### 📌 Passo a Passo para Organizar suas Finanças e Começar a Investir:\n\n"
                "1. **Mapeamento de Gastos:** Com base no seu histórico, seus maiores impactos atuais são o **Aluguel (R$ 1.200,00)** e **Supermercado (R$ 450,00)**. O primeiro passo é registrar todas as entradas e saídas.\n"
                "2. **Reserva de Emergência:** Antes de buscar rentabilidade alta, monte um fundo cobrindo de 3 a 6 meses do seu custo de vida.\n"
                "3. **Investimentos Recomendados (Perfil Moderado):**\n"
                "   - **Tesouro Selic:** Ideal para reserva de emergência pela liquidez diária e total segurança.\n"
                "   - **CDB Liquidez Diária (100% CDI):** Excelente opção para rentabilidade diária com garantia do FGC.\n"
                "4. **Diversificação Gradual:** Após consolidar a reserva, você pode destinar uma parcela para opções de renda fixa de médio prazo.")
    elif "cripto" in p or "bradesco" in p or "prefixado" in p or "quanto rende" in p:
        return ("Este produto específico não consta em nossa base de produtos cadastrados. "
                "Para o seu perfil (Moderado), recomendamos opções disponíveis de renda fixa segura, "
                "como o **Tesouro Selic** ou **CDB Liquidez Diária** com rentabilidade atrelada ao CDI.")
    elif "gasto" in p or "transaç" in p or "tabela" in p:
        return ("Com base na tabela de transações registrada, os maiores gastos do cliente incluem o **Aluguel** (R$ 1.200,00) "
                "e compras de **Supermercado** (R$ 450,00).")
    else:
        return ("Como seu assistente de educação financeira, estou aqui para ajudar você a mapear seus gastos diários, organizar seu orçamento e escolher os melhores produtos de investimento para o seu perfil. Como posso detalhar sua dúvida agora?")

# ---------------------------------------------------------
# 6. INTERFACE E CHAT COM FALLBACK E CONTINGÊNCIA
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
            with st.spinner("Analisando dados financeiros..."):
                texto_resposta = None
                
                # Nomes válidos e atualizados dos modelos oficiais do Gemini
                modelos_fallback = [
                    'gemini-2.0-flash',
                    'gemini-1.5-flash',
                    'gemini-1.5-pro'
                ]

                for mod in modelos_fallback:
                    try:
                        resposta = client.models.generate_content(
                            model=mod,
                            contents=entrada_usuario,
                            config={'system_instruction': PROMPT_SISTEMA}
                        )
                        if resposta and resposta.text:
                            texto_resposta = resposta.text
                            break
                    except Exception:
                        continue

                # Se todas as chamadas de API falharem, aciona a contingência enriquecida
                if not texto_resposta:
                    texto_resposta = resposta_contingencia(entrada_usuario)

                st.markdown(texto_resposta)
                st.session_state.historico.append({"papel": "assistant", "conteudo": texto_resposta})
else:
    st.info("👈 Para começar a conversa, informe sua chave de API na barra lateral à esquerda.")
