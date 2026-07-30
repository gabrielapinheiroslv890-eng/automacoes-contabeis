# Leitor de XML de Nota Fiscal Eletrônica (NF-e)

Script Python que lê arquivos XML de Notas Fiscais Eletrônicas e extrai os dados principais (fornecedor, CNPJ, produto, valores) pra uma planilha Excel.

## O problema

Toda NF-e emitida no Brasil gera um arquivo XML oficial, estruturado em tags aninhadas (não é uma planilha pronta). Conferir manualmente dezenas de notas, abrindo XML por XML, é inviável — automatizar a extração é uma das rotinas mais comuns de controladoria/contabilidade.

## A solução

1. `xml.etree.ElementTree` (biblioteca nativa do Python, sem instalação) lê a estrutura do XML
2. `glob` localiza todos os arquivos `.xml` de uma pasta automaticamente
3. Um laço `for` processa cada nota, navegando pela estrutura de tags (`infNFe/emit/xNome`, `infNFe/det/prod/vProd` etc.) pra extrair: número, data, fornecedor, CNPJ, destinatário, descrição do produto, valor do produto e valor total
4. Os dados de todas as notas são consolidados num único Excel (`notas_extraidas.xlsx`)

## Como usar

```bash
python ler_nfe.py
