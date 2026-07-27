# Leitor de Extrato Bancário em PDF

Script Python que extrai transações (data, descrição, valor) diretamente de um PDF de extrato bancário — sem precisar digitar ou copiar manualmente os dados pra uma planilha.

## O problema

Nem todo extrato bancário sai em Excel/CSV pronto pra usar — muitas vezes vem só em PDF. Copiar e colar isso manualmente numa planilha, linha por linha, é lento e sujeito a erro de digitação, especialmente em extratos longos.

## A solução

1. `pdfplumber` extrai o texto bruto do PDF, página por página
2. Um padrão de regex reconhece o formato `data + descrição + valor` em cada linha de texto
3. Um conversor de valores normaliza os formatos mais comuns usados por bancos diferentes:
   - `450,00` / `-35,90` (sinal de menos)
   - `R$ 450,00` (prefixo de moeda)
   - `(35,90)` (negativo entre parênteses)
   - `35,90 D` / `450,00 C` (sufixo Débito/Crédito em vez de sinal)
4. Linhas com números que não batem no padrão esperado (cabeçalho, rodapé, formato inesperado) são **sinalizadas no terminal**, não descartadas silenciosamente
5. Exporta pra `extrato_extraido.xlsx`, no mesmo formato (Data, Descrição, Valor) usado pelo projeto de [Conciliação Bancária](../conciliacao-bancaria) — os dois se conectam: extrai do PDF real e já usa na conciliação automática

## Como usar

```bash
python extrair_extrato_pdf.py caminho/do/extrato.pdf
