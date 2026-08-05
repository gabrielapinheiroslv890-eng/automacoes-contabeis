# Conciliação Bancária Automática

Automação em **Google Apps Script** que compara um extrato bancário com os lançamentos contábeis já registrados, identificando o que confere, o que está pendente e o que diverge — sem precisar bater manualmente linha por linha.

## O problema

Em rotinas contábeis, é comum ter que conferir se todo lançamento registrado tem um par correspondente no extrato do banco (e vice-versa). Feito manualmente, isso significa comparar dezenas ou centenas de linhas visualmente, o que é lento e sujeito a erro humano — principalmente quando existem valores repetidos (ex: várias mensalidades do mesmo valor em datas próximas).

## A solução

Uma planilha Google Sheets com 4 abas (`Extrato`, `Lançamentos`, `Conciliação`, `Histórico`) e um script Apps Script acionado por um menu customizado, que:

1. Lê as duas bases de dados (extrato e lançamentos)
2. Cruza cada linha do extrato com a lista de lançamentos por **valor exato** e **data próxima** (tolerância de 2 dias, configurável)
3. Quando duas ou mais linhas têm data e valor idênticos (ex: dois alunos pagando a mesma mensalidade no mesmo dia), desempata comparando as **palavras em comum na descrição** (ex: o nome do aluno) — evita que o script "roube" o par errado
4. Marca o resultado por cor: 🟢 conferido, 🟡 pendente (só no extrato), 🔴 só no lançamento
5. Gera um resumo automático com totais por status e o horário da última execução
6. **Registra um histórico**: cada execução acrescenta uma linha na aba "Histórico" (data/hora + contagem de cada status), sem apagar execuções anteriores — permite acompanhar ao longo do tempo se a qualidade dos lançamentos está melhorando

## Como usar

1. Preencher as abas `Extrato` e `Lançamentos` com data, descrição e valor
2. Menu `Conciliação → Rodar conciliação`
3. Conferir o resultado colorido na aba `Conciliação`, com o resumo no canto direito
4. Acompanhar a evolução ao longo do tempo na aba `Histórico`

## Stack

- Google Sheets
- Google Apps Script (JavaScript)

## Detalhes técnicos que valem destacar

- **Matching por score, não por primeiro encontrado**: a primeira versão pegava o primeiro candidato que batesse — o que causava pares errados quando havia valores duplicados na mesma data. A versão final calcula um "score" (diferença de dias, com desconto por palavras em comum na descrição) e escolhe sempre o melhor candidato disponível.
- **Sem duplicar pareamento**: um array `usados[]` garante que um lançamento não seja usado duas vezes para bater com dois itens do extrato.
- **Idempotente na conciliação, cumulativo no histórico**: rodar de novo sempre limpa e recalcula a aba "Conciliação" do zero, mas a aba "Histórico" **acrescenta** uma linha nova a cada execução (usando `getLastRow() + 1`), sem apagar o que já existia.

## Bugs encontrados e corrigidos (documentando o processo)

1. **TypeError ao rodar**: o arquivo do Apps Script ficou com conteúdo truncado após uma colagem incompleta — resolvido limpando o editor por completo antes de colar o código novo.
2. **Pareamento errado com valores duplicados**: dois lançamentos no mesmo dia e mesmo valor faziam o script casar com a pessoa errada. Resolvido adicionando um critério de desempate por similaridade de descrição.
3. **Chave `{` não fechada** ao criar a função de histórico: o `registrarHistorico()` foi escrito sem o `}` de fechamento no final, causando `SyntaxError: Unexpected end of input`.
4. **Variável usada sem ser declarada**: sobrou uma referência a `valores[status] += valor` copiada de outra função, sem que `valores` tivesse sido declarada na função nova — removida por não ser necessária pro histórico (só contagem, não soma em R$).
5. **Testar a função errada isoladamente**: rodar `registrarHistorico` diretamente pelo botão "Executar" falha, porque essa função depende de receber `resultado` como argumento — algo que só acontece quando ela é chamada de dentro da `conciliar()`. Lição: pra testar uma função que depende de parâmetros vindos de outra, é preciso rodar a função "de entrada" (nesse caso, `conciliar`), não a função interna isolada.

## Próximos incrementos possíveis

- Importar CSV do banco diretamente, em vez de colar manual
- Matching fuzzy na descrição (Levenshtein) para nomes com pequenas variações de escrita
- Gráfico de evolução das divergências ao longo do tempo, a partir da aba "Histórico"

## Código

Ver [`conciliacao.gs`](./conciliacao.gs).
