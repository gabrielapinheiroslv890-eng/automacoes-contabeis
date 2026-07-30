# Painel Financeiro — Contas a Pagar e Receber (Power BI)

Dashboard Power BI com modelo de dados relacional (5 tabelas) mostrando o saldo entre contas a pagar e contas a receber, com detalhamento por fornecedor, por cliente e evolução mensal.

## O problema

Controlar contas a pagar e a receber junto exige cruzar dados de fontes diferentes (fornecedores, clientes, lançamentos de cada tipo) e enxergar o saldo líquido do período — não só os totais isolados. Fazer isso em planilha única, sem um modelo relacional, vira uma bagunça de VLOOKUPs.

## A solução

Um modelo de dados em **esquema estrela**: duas tabelas de fato (`Contas a Pagar`, `Contas a Receber`) ligadas a três tabelas de dimensão (`Fornecedores`, `Clientes`, `Calendário`).

### Relacionamentos
