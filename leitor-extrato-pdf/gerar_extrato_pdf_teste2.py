"""
Gera um segundo PDF de extrato de teste, simulando um banco com formato
DIFERENTE do primeiro (R$, parênteses pra negativo, sufixo D/C) — usado
pra validar que o extrator lida com múltiplos formatos de valor.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

ARQUIVO_SAIDA = "extrato_banco2.pdf"

# formato diferente do banco 1: usa R$, parênteses e sufixo D/C
TRANSACOES = [
    ("01/08/2026", "TRANSFERENCIA RECEBIDA CLIENTE A", "R$ 850,00 C"),
    ("03/08/2026", "TARIFA PACOTE SERVICOS", "(29,90)"),
    ("05/08/2026", "PAGAMENTO NF FORNECEDOR B", "R$ 1.500,00 D"),
    ("08/08/2026", "PIX RECEBIDO CLIENTE C", "R$ 850,00 C"),
    ("12/08/2026", "IOF SOBRE APLICACAO", "(4,20)"),
]


def gerar_pdf():
    c = canvas.Canvas(ARQUIVO_SAIDA, pagesize=A4)
    largura, altura = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, altura - 50, "Extrato de Conta - Banco Exemplo 2")

    y = altura - 90
    c.setFont("Helvetica", 10)
    for data, descricao, valor in TRANSACOES:
        c.drawString(50, y, data)
        c.drawString(150, y, descricao)
        c.drawRightString(520, y, valor)
        y -= 18

    c.save()
    print(f"PDF de teste (formato 2) gerado: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    gerar_pdf()
