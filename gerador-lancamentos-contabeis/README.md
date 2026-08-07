# Gerador de Lançamentos Contábeis (Python)

Script Python que lê uma planilha de despesas e gera automaticamente os lançamentos contábeis (débito/crédito) em partida dobrada, exportando para um Excel pronto.

## O problema

Lançar despesas manualmente exige decidir, pra cada nota/fatura, qual conta contábil debitar — um trabalho repetitivo e sujeito a erro de digitação ou de classificação, especialmente em volume.

## A solução

Uma planilha `despesas.xlsx` com as despesas do período e uma planilha `plano_contas.xlsx` com o de-para de categoria → conta contábil — **editável sem mexer no código**. O script cruza as duas, gera o lançamento (débito na conta da categoria, crédito numa conta bancária padrão) e valida que a partida dobrada fecha (soma dos débitos = soma dos créditos). Categorias sem conta cadastrada caem automaticamente em "A CLASSIFICAR", nunca são lançadas com uma conta inventada.

## Como usar

Os nomes dos arquivos de entrada são passados na hora de rodar (não fixos no código):

```bash
python gerador_lancamentos.py despesas.xlsx plano_contas.xlsx
