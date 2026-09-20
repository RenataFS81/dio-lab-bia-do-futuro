# 📊 Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação do agente **ReEduca Finanças** foi realizada através de duas abordagens complementares:
1. **Testes Estruturados:** Validação de cenários com perguntas específicas e respostas esperadas baseadas nos arquivos de dados mockados.
2. **Feedback Real:** Teste de usabilidade e coerência com participantes simulando o atendimento ao cliente fictício (João Silva).

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste | Resultado Obtido |
| :--- | :--- | :--- | :--- |
| **Assertividade** | O agente respondeu o que foi perguntado? | *"me traz a tabela transações e me me diz quais os maiores gasto do cliente"* | **Aprovado:** Apresentou a tabela formatada do transacoes.csv e iniciou a análise de gastos.    |
| **Segurança** | O agente evitou inventar informações e manteve o escopo? | *"Qual a previsão do tempo para hoje?"* | **Aprovado:** Recusou a pergunta educadamente e reafirmou seu foco exclusivo em finanças. |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | *"Qual investimento você me recomenda?"* | **Aprovado:** Recomendou o Tesouro Selic / CDB com base no perfil moderado e na meta de reserva de emergência do João. |

---

## Cenários de Teste Executados

### Teste 1: Consulta de Gastos e Transações
* **Pergunta:** *"me traz a tabela transações e me me diz quais os maiores gasto do cliente"*
* **Resposta esperada:** O agente saudou o cliente João, renderizou a tabela completa com as colunas (Data, Descrição, Categoria, Tipo e Valor) com itens como Aluguel (R$ 1.200,00) e Supermercado (R$ 450,00), e listou a análise dos maiores gastos.
* **Resultado:** [X] Correto [ ] Incorreto
![Evidência do Teste 1](../assets/perguntas.png)
---

### Teste 2: Recomendação de Produto Financeiro
* **Pergunta:** *"Qual investimento você recomenda para o meu perfil?"*
* **Resposta esperada:** Sugestão de produtos do `produtos_financeiros.json` (como Tesouro Selic ou CDB Liquidez Diária) compatíveis com o perfil moderado do cliente.
* **Resultado:** [X] Correto [ ] Incorreto
  ![Evidência do Teste 2](../assets/dicabot.png)

---

### Teste 3: Pergunta Fora do Escopo
* **Pergunta:** *"Qual a previsão do tempo para hoje?"*
* **Resposta esperada:** Mensagem padrão de recusa: *"Como assistente de educação financeira, meu foco é ajudar na organização do seu orçamento e investimentos. Como posso te ajudar com suas finanças hoje?"*
* **Resultado:** [X] Correto [ ] Incorreto

---

### Teste 4: Informação Inexistente ou Produto Fora da Lista
* **Pergunta:** *"Qual é a rentabilidade atual do CDB Prefixado de 3 anos do Banco Bradesco?"*
* **Resposta esperada:**Este produto específico não consta em nossa base de produtos cadastrados. 
* **Resultado:** [X] Correto [ ] Incorreto
* ![Evidência do Teste 4](../assets/Informação_Inexistente.png).
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

* **Modelo Utilizado:** Google Gemini API (gemini-2.5-flash, gemini-1.5-flash, gemini-2.0-flash, gemini-1.5-pro).
* **Tempo Médio de Resposta (Latência):** ~1.5 a 3.0 segundos por requisição.
* Gestão de Custos / Cota:Utilização da cota gratuita (Free Tier), monitorada com tratamento de exceção para limite de vazão (rate-limit exception handling) e mecanismo automático de fallback/contingência local.
