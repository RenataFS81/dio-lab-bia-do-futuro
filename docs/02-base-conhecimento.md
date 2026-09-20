# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores |
| `perfil_investidor.json` | JSON | Personalizar recomendações |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

[Não modifiquei a estrutura base, utilizei os arquivos indicados para o desafio (perfil_investidor.json, produtos_financeiros.json, transacoes.csv e historico_atendimento.csv).]

---

## Estratégia de Integração

### Como os dados são carregados?
> Os dados estruturados (JSON) e tabulares (CSV) são lidos localmente na inicialização do script através de uma função auxiliar (carregar_dados()). Os ficheiros JSON são lidos diretamente e os ficheiros CSV são processados via biblioteca Pandas e convertidos para representação textual em tabela (to_string()).

### Como os dados são usados no prompt?
> Os dados são injetados diretamente no system_instruction (System Prompt) da API do Gemini (gemini-3.6-flash). Dessa forma, a base de conhecimento do cliente e os produtos disponíveis ficam na memória de contexto do modelo desde a primeira mensagem.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Você é o "ReEduca Finanças", um agente de IA especialista em consultoria e educação financeira no Brasil.

DADOS DO CLIENTE E DO SISTEMA:
- PERFIL DO CLIENTE:
{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.0,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Construir reserva de emergência"
}

- PRODUTOS FINANCEIROS:
[
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic"
  }
]

- TRANSAÇÕES REGISTRADAS:
id_transacao  data       categoria     descricao            valor_brl  tipo
1001          2026-09-01 Alimentação   Supermercado         450.0      Saída
1003          2026-09-05 Renda         Salário / Proventos  3500.0     Entrada

- HISTÓRICO DE ATENDIMENTOS:
id_atendimento data       categoria     resumo_atendimento                             status
1              2026-08-10 Dívidas       Cliente solicitou plano de renegociação        Concluído

DIRETRIZES:
1. Responda com base nos dados do cliente acima.
2. Se o usuário perguntar sobre os gastos do João ou maiores despesas, analise a lista de transações e detalhe os valores.
```
