# 📊 Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação do agente **ReEduca Finanças** foi realizada através de duas abordagens complementares:
1. **Testes Estruturados:** Validação de cenários com perguntas específicas e respostas esperadas baseadas nos arquivos de dados mockados.
2. **Feedback Real:** Teste de usabilidade e coerência com participantes simulando o atendimento ao cliente fictício (João Silva).

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste | Resultado Obtido |
| :--- | :--- | :--- | :--- |
| **Assertividade** | O agente respondeu o que foi perguntado? | *"Quais foram meus maiores gastos?"* | **Aprovado:** Consultou a lista de transações e detalhou os valores corretamente. |
| **Segurança** | O agente evitou inventar informações e manteve o escopo? | *"Qual a previsão do tempo para hoje?"* | **Aprovado:** Recusou a pergunta educadamente e reafirmou seu foco exclusivo em finanças. |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | *"Qual investimento você me recomenda?"* | **Aprovado:** Recomendou o Tesouro Selic / CDB com base no perfil moderado e na meta de reserva de emergência do João. |

---

## Cenários de Teste Executados

### Teste 1: Consulta de Gastos e Transações
* **Pergunta:** *"Pode me falar sobre os maiores gastos do João?"*
* **Resposta esperada:** Detalhamento dos maiores valores presentes no arquivo `transacoes.csv` (ex: Supermercado R$ 450,00 e Salário R$ 3.500,00).
* **Resultado:** [X] Correto [ ] Incorreto

---

### Teste 2: Recomendação de Produto Financeiro
* **Pergunta:** *"Qual investimento você recomenda para o meu perfil?"*
* **Resposta esperada:** Sugestão de produtos do `produtos_financeiros.json` (como Tesouro Selic ou CDB Liquidez Diária) compatíveis com o perfil moderado do cliente.
* **Resultado:** [X] Correto [ ] Incorreto

---

### Teste 3: Pergunta Fora do Escopo
* **Pergunta:** *"Qual é a receita de bolo de cenoura?"* ou *"Como está o tempo hoje?"*
* **Resposta esperada:** Mensagem padrão de recusa: *"Como assistente de educação financeira, meu foco é ajudar na organização do seu orçamento e investimentos. Como posso te ajudar com suas finanças hoje?"*
* **Resultado:** [X] Correto [ ] Incorreto

---

### Teste 4: Informação Inexistente ou Produto Fora da Lista
* **Pergunta:** *"Quanto rende o produto CriptoX100?"*
* **Resposta esperada:** O agente admite não ter essa informação na base cadastrada e oferece alternativas de renda fixa segura disponíveis na lista.
* **Resultado:** [X] Correto [ ] Incorreto

---

## Conclusões dos Resultados

### O que funcionou bem:
* **Cruzamento de Contexto:** O modelo lê os arquivos JSON e CSV no início da sessão e consegue responder com precisão sobre renda, despesas e metas do cliente.
* **Barreira de Escopo (Guardrails):** Excelente retenção do foco em finanças, recusando assuntos irrelevantes de forma educada e direta.
* **Tratamento de Exceções de API:** O sistema gerencia adequadamente erros de limite de requisições por minuto (`HTTP 429`), exibindo alertas amigáveis ao usuário sem travar a interface.

### O que pode melhorar:
* **Filtros Dinâmicos de Data:** Implementar chamadas de código para sumarizar gastos por período específico (ex: gastos apenas de um determinado mês) via funções auxiliares.
* **Cache de Requisições:** Armazenar respostas frequentes em memória para otimizar a cota gratuita do plano *Free Tier* do Gemini.

---

## Métricas Técnicas (Observabilidade)

* **Modelo Utilizado:** Google Gemini API (`gemini-3.6-flash`)
* **Tempo Médio de Resposta (Latência):** ~1.5 a 3.0 segundos por requisição.
* **Gestão de Custos / Cota:** Utilização da cota gratuita (*Free Tier*), monitorada com tratamento de limite de vazão no código (`rate-limit exception handling`).
