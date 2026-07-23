# Conciliação Bancária Automática

Automação em **Google Apps Script** que compara um extrato bancário com os lançamentos contábeis já registrados, identificando o que confere, o que está pendente e o que diverge — sem precisar bater manualmente linha por linha.

## O problema

Em rotinas contábeis, é comum ter que conferir se todo lançamento registrado tem um par correspondente no extrato do banco (e vice-versa). Feito manualmente, isso significa comparar dezenas ou centenas de linhas visualmente, o que é lento e sujeito a erro humano — principalmente quando existem valores repetidos (ex: várias mensalidades do mesmo valor em datas próximas).

## A solução

Uma planilha Google Sheets com 3 abas (`Extrato`, `Lançamentos`, `Conciliação`) e um script Apps Script acionado por um menu customizado, que:

1. Lê as duas bases de dados (extrato e lançamentos)
2. Cruza cada linha do extrato com a lista de lançamentos por **valor exato** e **data próxima** (tolerância de 2 dias, configurável)
3. Quando duas ou mais linhas têm data e valor idênticos (ex: dois alunos pagando a mesma mensalidade no mesmo dia), desempata comparando as **palavras em comum na descrição** (ex: o nome do aluno) — evita que o script "roube" o par errado
4. Marca o resultado por cor: 🟢 conferido, 🟡 pendente (só no extrato), 🔴 só no lançamento
5. Gera um resumo automático com totais por status e o horário da última execução

## Como usar

1. Preencher as abas `Extrato` e `Lançamentos` com data, descrição e valor
2. Menu `Conciliação → Rodar conciliação`
3. Conferir o resultado colorido na aba `Conciliação`, com o resumo no canto direito

## Stack

- Google Sheets
- Google Apps Script (JavaScript)

## Detalhes técnicos que valem destacar

- **Matching por score, não por primeiro encontrado**: a primeira versão pegava o primeiro candidato que batesse — o que causava pares errados quando havia valores duplicados na mesma data. A versão final calcula um "score" (diferença de dias, com desconto por palavras em comum na descrição) e escolhe sempre o melhor candidato disponível.
- **Sem duplicar pareamento**: um array `usados[]` garante que um lançamento não seja usado duas vezes para bater com dois itens do extrato.
- **Idempotente**: rodar de novo sempre limpa e recalcula do zero, não acumula lixo de execuções anteriores.

## Bugs encontrados e corrigidos (documentando o processo)

1. **TypeError ao rodar**: o arquivo do Apps Script ficou com conteúdo truncado após uma colagem incompleta — resolvido limpando o editor por completo antes de colar o código novo.
2. **Pareamento errado com valores duplicados**: dois lançamentos no mesmo dia e mesmo valor faziam o script casar com a pessoa errada. Resolvido adicionando um critério de desempate por similaridade de descrição.

## Próximos incrementos possíveis

- Importar CSV do banco diretamente, em vez de colar manual
- Matching fuzzy na descrição (Levenshtein) para nomes com pequenas variações de escrita
- Histórico de execuções (log de quando e quantas divergências cada rodada encontrou)

## Código

Ver [`conciliacao.gs`](./conciliacao.gs).
