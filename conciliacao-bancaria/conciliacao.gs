/**
 * Concilia a aba "Extrato" com a aba "Lançamentos" por Data + Valor.
 * Escreve o resultado na aba "Conciliação".
 */
function conciliar() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const abaExtrato = ss.getSheetByName('Extrato');
  const abaLancamentos = ss.getSheetByName('Lançamentos');
  const abaConciliacao = ss.getSheetByName('Conciliação');

  const extrato = lerDados(abaExtrato);
  const lancamentos = lerDados(abaLancamentos);

  // marca quais lançamentos já foram usados, pra não casar duas vezes com o mesmo
  const usados = new Array(lancamentos.length).fill(false);
  const TOLERANCIA_DIAS = 2;

  const resultado = [];

  extrato.forEach(linhaExtrato => {
    const idx = encontrarCorrespondencia(linhaExtrato, lancamentos, usados, TOLERANCIA_DIAS);

    if (idx === -1) {
      resultado.push([
        linhaExtrato.data, linhaExtrato.descricao, linhaExtrato.valor,
        'PENDENTE', '', ''
      ]);
    } else {
      usados[idx] = true;
      const match = lancamentos[idx];
      resultado.push([
        linhaExtrato.data, linhaExtrato.descricao, linhaExtrato.valor,
        'CONFERIDO', match.data, match.descricao
      ]);
    }
  });

  // lançamentos que sobraram sem par no extrato = também divergência
  lancamentos.forEach((lanc, idx) => {
    if (!usados[idx]) {
      resultado.push(['', '', '', 'SÓ NO LANÇAMENTO', lanc.data, lanc.descricao]);
    }
  });

  escreverResultado(abaConciliacao, resultado);
  escreverResumo(abaConciliacao, resultado);
}

function lerDados(aba) {
  const valores = aba.getDataRange().getValues();
  const linhas = valores.slice(1); // pula cabeçalho
  return linhas
    .filter(l => l[0] !== '') // ignora linhas vazias
    .map(l => ({ data: new Date(l[0]), descricao: l[1], valor: Number(l[2]) }));
}

function encontrarCorrespondencia(alvo, lista, usados, toleranciaDias) {
  // escolhe o candidato com melhor "score": data mais próxima é o critério
  // principal; similaridade de descrição desempata quando duas datas/valores
  // são idênticos (ex: duas mensalidades de R$ 450 no mesmo dia)
  let melhorIdx = -1;
  let melhorScore = Infinity;

  for (let i = 0; i < lista.length; i++) {
    if (usados[i]) continue;
    const candidato = lista[i];

    const valorBate = Math.abs(candidato.valor - alvo.valor) < 0.01;
    if (!valorBate) continue;

    const diffDias = Math.abs((candidato.data - alvo.data) / (1000 * 60 * 60 * 24));
    if (diffDias > toleranciaDias) continue;

    const palavrasComuns = contarPalavrasComuns(alvo.descricao, candidato.descricao);
    // cada palavra em comum (ex: nome do aluno) reduz o score em 0.1,
    // suficiente pra desempatar sem nunca superar uma diferença real de dias
    const score = diffDias - palavrasComuns * 0.1;

    if (score < melhorScore) {
      melhorScore = score;
      melhorIdx = i;
    }
  }

  return melhorIdx;
}

function normalizarTexto(texto) {
  return texto
    .toString()
    .toUpperCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, ''); // remove acentos
}

function contarPalavrasComuns(descricaoA, descricaoB) {
  const palavrasA = normalizarTexto(descricaoA).split(/\s+/).filter(p => p.length > 2);
  const palavrasB = normalizarTexto(descricaoB).split(/\s+/).filter(p => p.length > 2);
  return palavrasA.filter(p => palavrasB.includes(p)).length;
}

function escreverResultado(aba, resultado) {
  aba.getRange(2, 1, aba.getMaxRows() - 1, 6).clearContent();
  aba.getRange(2, 1, aba.getMaxRows() - 1, 6).setBackground(null);

  if (resultado.length === 0) return;

  const range = aba.getRange(2, 1, resultado.length, 6);
  range.setValues(resultado);

  // colore por status (coluna D, índice 4)
  for (let i = 0; i < resultado.length; i++) {
    const status = resultado[i][3];
    const linha = aba.getRange(i + 2, 4);
    if (status === 'CONFERIDO') linha.setBackground('#d9ead3');       // verde
    else if (status === 'PENDENTE') linha.setBackground('#fff2cc');   // amarelo
    else linha.setBackground('#f4cccc');                              // vermelho
  }
}

/**
 * Escreve um resumo com totais por status na coluna H/I, sem mexer
 * na área de dados principal (colunas A-F).
 */
function escreverResumo(aba, resultado) {
  const contagem = { CONFERIDO: 0, PENDENTE: 0, 'SÓ NO LANÇAMENTO': 0 };
  const valores = { CONFERIDO: 0, PENDENTE: 0, 'SÓ NO LANÇAMENTO': 0 };

  resultado.forEach(linha => {
    const status = linha[3];
    // valor pode estar na coluna de extrato (índice 2) ou não existir (linha só-lançamento)
    const valor = typeof linha[2] === 'number' ? linha[2] : 0;
    contagem[status]++;
    valores[status] += valor;
  });

  const linhasResumo = [
    ['Resumo da conciliação', ''],
    ['Conferidos', contagem.CONFERIDO + ' (R$ ' + valores.CONFERIDO.toFixed(2) + ')'],
    ['Pendentes (só no extrato)', contagem.PENDENTE + ' (R$ ' + valores.PENDENTE.toFixed(2) + ')'],
    ['Só no lançamento', contagem['SÓ NO LANÇAMENTO'] + ''],
    ['Total de linhas', resultado.length],
    ['Última execução', Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'dd/MM/yyyy HH:mm')]
  ];

  const range = aba.getRange(1, 8, linhasResumo.length, 2); // começa em H1
  range.setValues(linhasResumo);
  aba.getRange(1, 8, 1, 2).setFontWeight('bold').setBackground('#d9d2e9');
}

/**
 * Adiciona um menu customizado "Conciliação" na planilha.
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Conciliação')
    .addItem('Rodar conciliação', 'conciliar')
    .addToUi();
}
