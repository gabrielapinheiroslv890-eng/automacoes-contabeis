"""
Gera um PDF de extrato bancário fictício, só pra servir de dado de teste
pro script `extrair_extrato_pdf.py`. Simula o formato de texto comum em
extratos exportados por bancos (data, descrição, valor).
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

ARQUIVO_SAIDA = "extrato_banco.pdf"

TRANSACOES = [
    ("01/07/2026", "PIX RECEBIDO - ALUNO JOAO", "450,00"),
    ("02/07/2026", "TARIFA MANUTENCAO CONTA", "-35,90"),
    ("03/07/2026", "PAGAMENTO FORNECEDOR XYZ", "-1200,00"),
    ("05/07/2026", "PIX RECEBIDO - ALUNO MARIA", "450,00"),
    ("07/07/2026", "TED RECEBIDA - CONVENIO ABC", "3000,00"),
    ("10/07/2026", "PAGAMENTO BOLETO ALUGUEL", "-2500,00"),
    ("12/07/2026", "DEVOLUCAO PIX - ERRO", "120,00"),
    ("15/07/2026", "PAGAMENTO FOLHA - ADIANTAMENTO", "-5400,00"),
    ("18/07/2026", "PIX RECEBIDO - ALUNO PEDRO", "450,00"),
    ("20/07/2026", "TARIFA DOC", "-12,50"),
]


def gerar_pdf():
    c = canvas.Canvas(ARQUIVO_SAIDA, pagesize=A4)
    largura, altura = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, altura - 50, "Extrato Bancário - Conta Corrente 12345-6")

    c.setFont("Helvetica", 10)
    c.drawString(50, altura - 70, "Período: 01/07/2026 a 31/07/2026")

    y = altura - 110
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Data")
    c.drawString(150, y, "Histórico")
    c.drawString(450, y, "Valor")

    c.setFont("Helvetica", 10)
    y -= 20
    for data, descricao, valor in TRANSACOES:
        c.drawString(50, y, data)
        c.drawString(150, y, descricao)
        c.drawRightString(520, y, valor)
        y -= 18

    c.save()
    print(f"PDF de teste gerado: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    gerar_pdf()
