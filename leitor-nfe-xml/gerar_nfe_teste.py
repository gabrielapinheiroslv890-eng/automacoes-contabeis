"""
Gera arquivos XML de NF-e fictícios (formato simplificado, mas com as
tags reais mais importantes), pra servir de dado de teste pro leitor.
"""

NOTAS = [
    {
        "numero": "1001", "data": "2026-07-01",
        "fornecedor": "Papelaria Central Ltda", "cnpj": "12.345.678/0001-90",
        "produto": "Material de escritório diverso", "valor_produto": "340.00",
        "valor_total": "340.00",
    },
    {
        "numero": "1002", "data": "2026-07-05",
        "fornecedor": "Ar Condicionado Express ME", "cnpj": "98.765.432/0001-10",
        "produto": "Manutenção preventiva ar condicionado", "valor_produto": "650.00",
        "valor_total": "650.00",
    },
    {
        "numero": "1003", "data": "2026-07-12",
        "fornecedor": "Grafica Rapida EIRELI", "cnpj": "11.222.333/0001-44",
        "produto": "Impressão de material gráfico", "valor_produto": "150.00",
        "valor_total": "150.00",
    },
]

XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<NFe>
  <infNFe>
    <ide>
      <nNF>{numero}</nNF>
      <dhEmi>{data}T10:00:00-03:00</dhEmi>
    </ide>
    <emit>
      <xNome>{fornecedor}</xNome>
      <CNPJ>{cnpj}</CNPJ>
    </emit>
    <dest>
      <xNome>Empresa Destinataria Exemplo Ltda</xNome>
    </dest>
    <det nItem="1">
      <prod>
        <xProd>{produto}</xProd>
        <vProd>{valor_produto}</vProd>
      </prod>
    </det>
    <total>
      <ICMSTot>
        <vNF>{valor_total}</vNF>
      </ICMSTot>
    </total>
  </infNFe>
</NFe>
"""

for nota in NOTAS:
    conteudo = XML_TEMPLATE.format(**nota)
    nome_arquivo = f"nfe_{nota['numero']}.xml"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"Gerado: {nome_arquivo}")
