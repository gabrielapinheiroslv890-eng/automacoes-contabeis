# Automações Contábeis

Portfólio de automações voltadas pra rotinas contábeis, construídas como estudante da área explorando Google Apps Script, Python e Power BI.

## Projetos

### 1. [Conciliação Bancária Automática](./conciliacao-bancaria)
Google Apps Script que cruza extrato bancário com lançamentos contábeis, identificando o que confere, o que está pendente e o que diverge — com desempate inteligente quando há valores repetidos.

**Stack:** Google Sheets, Apps Script

### 2. [Gerador de Lançamentos Contábeis](./gerador-lancamentos-contabeis)
Script Python que lê uma planilha de despesas e gera lançamentos contábeis em partida dobrada, classificando por um plano de contas editável em planilha separada.

**Stack:** Python, pandas

### 3. [Dashboard de Apuração de Impostos](./dashboard-apuracao-impostos)
Cálculo da apuração mensal do Simples Nacional (Anexo III) em Python, visualizado num dashboard Power BI com evolução do imposto e mudança de faixa ao longo do tempo.

### 4. [Leitor de Extrato Bancário em PDF](./leitor-extrato-pdf)
Extração automática de transações (data, descrição, valor) de PDFs de extrato bancário, com suporte a múltiplos formatos de valor usados por bancos diferentes. Se conecta com o Projeto 1 (conciliação bancária).

**Stack:** Python, pdfplumber

### 5. [App de Geração de Lançamentos (Streamlit)](./app-gerador-lancamentos)
Interface web sobre o Projeto 2, com upload de arquivo, cards de métrica e download do resultado — leva a mesma lógica de terminal pra um aplicativo usável por qualquer pessoa.

**Stack:** Python, Streamlit

### 6. [Painel Financeiro — Contas a Pagar e Receber (Power BI avançado)](./dashboard-financeiro-avancado)
Modelo de dados relacional (5 tabelas, esquema estrela) com medidas DAX e visuais cruzando fornecedores, clientes e saldo do período.

**Stack:** Power BI, DAX

### 7. [Leitor de XML de Nota Fiscal Eletrônica (NF-e)](./leitor-nfe-xml)
Extração automática de dados de notas fiscais a partir do XML oficial (número, fornecedor, CNPJ, valores), consolidando várias notas num único Excel.
**Stack:** Python, xml.etree.ElementTree

**Stack:** Python, Power BI

## Sobre

Cada projeto tem seu próprio README com: o problema que resolve, como a solução funciona, decisões técnicas relevantes e bugs reais encontrados e corrigidos durante o desenvolvimento — documentando não só o resultado final, mas o processo.
