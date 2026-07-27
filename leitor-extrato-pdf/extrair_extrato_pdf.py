"""
Extrator de Extrato Bancário em PDF.

Lê um PDF de extrato bancário (texto, não digitalizado/escaneado) e
extrai as transações (Data, Descrição, Valor) usando um padrão de regex,
exportando pra `extrato_extraido.xlsx` — no mesmo formato usado pelo
projeto de Conciliação Bancária (aba "Extrato").

Suporta variações comuns de formatação de valor entre bancos:
- "450,00" / "-35,90" (sinal de menos)
- "R$ 450,00" (prefixo de moeda)
- "(35,90)" (negativo entre parênteses)
- "35,90 D" / "450,00 C" (sufixo Débito/Crédito em vez de sinal)
- "450.00" (decimal com ponto, formato americano)
"""

import re
import sys

import pandas as pd
import pdfplumber

ARQUIVO_SAIDA = "extrato_extraido.xlsx"

# casa linhas como: 01/07/2026   PIX RECEBIDO - ALUNO JOAO   450,00
# o grupo de valor é permissivo o suficiente pra pegar "R$ 450,00", "(35,90)", "35,90 D" etc.
PADRAO_LINHA = re.compile(
    r"^(\d{2}/\d{2}/\d{4})\s+(.+?)\s+((?:R\$\s*)?\(?-?[\d.,]+\)?(?:\s*[DC])?)$"
)


def extrair_texto(caminho_pdf):
    linhas = []
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text() or ""
            linhas.extend(texto.split("\n"))
    return linhas


def converter_valor(valor_bruto):
    """Normaliza os formatos de valor mais comuns em extratos bancários
    (BR, com R$, com parênteses, com sufixo D/C) pra float com sinal."""
    texto = valor_bruto.strip()
    negativo = False

    texto = re.sub(r"^R\$\s*", "", texto)

    if texto.startswith("(") and texto.endswith(")"):
        negativo = True
        texto = texto[1:-1].strip()

    if texto.upper().endswith(" D"):
        negativo = True
        texto = texto[:-2].strip()
    elif texto.upper().endswith(" C"):
        texto = texto[:-2].strip()

    if texto.startswith("-"):
        negativo = True
        texto = texto[1:].strip()

    # se tem vírgula, assume formato BR (ponto = milhar, vírgula = decimal)
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")

    valor = float(texto)
    return -abs(valor) if negativo else valor


def extrair_transacoes(linhas):
    transacoes = []
    linhas_nao_reconhecidas = []

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        match = PADRAO_LINHA.match(linha)
        if match:
            data, descricao, valor_bruto = match.groups()
            try:
                valor = converter_valor(valor_bruto)
            except ValueError:
                linhas_nao_reconhecidas.append(linha)
                continue

            transacoes.append({
                "Data": data,
                "Descrição": descricao.strip(),
                "Valor": valor,
            })
        elif re.search(r"\d", linha):
            linhas_nao_reconhecidas.append(linha)

    return pd.DataFrame(transacoes), linhas_nao_reconhecidas


def main():
    if len(sys.argv) < 2:
        print("Uso: python extrair_extrato_pdf.py <caminho_do_pdf>")
        sys.exit(1)

    caminho_pdf = sys.argv[1]
    linhas = extrair_texto(caminho_pdf)
    transacoes, nao_reconhecidas = extrair_transacoes(linhas)

    if transacoes.empty:
        print("Nenhuma transação foi reconhecida. Confira o padrão do PDF de entrada.")
        sys.exit(1)

    transacoes.to_excel(ARQUIVO_SAIDA, index=False)

    print(f"{len(transacoes)} transações extraídas em '{ARQUIVO_SAIDA}'.")
    print(f"Total: R$ {transacoes['Valor'].sum():,.2f}")

    if nao_reconhecidas:
        print(f"\nATENÇÃO: {len(nao_reconhecidas)} linha(s) com números não foram reconhecidas como transação:")
        for linha in nao_reconhecidas:
            print(f"  - {linha}")


if __name__ == "__main__":
    main()
