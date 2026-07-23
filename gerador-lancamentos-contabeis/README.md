# Gerador de Lançamentos Contábeis (Python)

Script em Python que lê uma planilha de despesas e gera automaticamente os lançamentos contábeis correspondentes (débito/crédito, em partida dobrada), prontos para importar num sistema contábil.

## O problema

Lançar despesas manualmente exige decidir, pra cada nota/fatura, qual conta contábil debitar — um trabalho repetitivo e sujeito a erro de digitação ou de classificação, especialmente em volume.

## A solução

1. Uma planilha `despesas.xlsx` com as despesas do período (Data, Fornecedor, Categoria, Valor)
2. Uma planilha `plano_contas.xlsx` com o de-para de categoria → conta contábil — **editável sem mexer no código**
3. Um script Python que cruza as duas, gera o lançamento (débito na conta da categoria, crédito na conta bancária padrão) e valida que a partida dobrada fecha (soma dos débitos = soma dos créditos)
4. Categorias sem conta cadastrada caem automaticamente em "A CLASSIFICAR", nunca são lançadas com uma conta inventada

## Como usar

1. Preencher `despesas.xlsx` e `plano_contas.xlsx`
2. Rodar `python gerador_lancamentos.py`
3. Conferir `lancamentos_gerados.xlsx` — e o resumo impresso no terminal (total lançado, quantos precisam de revisão)

## Stack

- Python 3
- pandas + openpyxl (leitura/escrita de Excel)

## Detalhes técnicos que valem destacar

- **Plano de contas desacoplado do código**: a primeira versão tinha o dicionário de contas fixo no script. Foi refeito pra ler de uma planilha externa — assim quem não programa consegue cadastrar conta nova sem editar Python.
- **Nunca lança em conta desconhecida**: categorias sem match caem em `9.9.9 - A CLASSIFICAR`, sinalizadas na coluna `Precisa Revisão`, em vez de o script travar ou chutar uma conta.
- **Validação de partida dobrada**: o script confere que soma de débitos = soma de créditos antes de exportar — é o princípio contábil básico, aplicado como guarda de qualidade do dado gerado.

## Bug real encontrado

Ao rodar o script uma segunda vez com o arquivo de saída ainda aberto no Excel, o Python falhou com `PermissionError: [Errno 13] Permission denied` — o Windows bloqueia escrita em arquivo aberto por outro programa. Resolvido fechando o Excel antes de rodar novamente. (Não é bug do script — é um comportamento do sistema operacional que vale documentar pra quem for usar.)

## Próximos incrementos possíveis

- Suportar múltiplas formas de pagamento (Caixa vs Fornecedores a Pagar) em vez de conta de crédito fixa
- Exportar direto no formato de importação do sistema contábil usado (ex: layout Alterdata)
- Interface simples (linha de comando com argumentos) pra escolher os arquivos de entrada sem editar o script

## Código

Ver [`gerador_lancamentos.py`](./gerador_lancamentos.py).
