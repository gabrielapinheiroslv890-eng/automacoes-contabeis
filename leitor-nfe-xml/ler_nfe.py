import glob
import xml.etree.ElementTree as ET
arquivos = glob.glob("leitor-nfe-xml/*.xml")

notas = []
import pandas as pd
df = pd.DataFrame(notas)
df.to_excel("notas_extraidas.xlsx", index=False)
for arquivo in arquivos:
    tree = ET.parse(arquivo)
    root = tree.getroot()
    print(root.tag)
    numero = root.find("infNFe/ide/nNF").text
    print(numero)

    data = root.find("infNFe/ide/dhEmi").text
    print(data)

    nome_fornecedor = root.find("infNFe/emit/xNome").text
    print (nome_fornecedor)

    cnpj_fornecedor = root.find("infNFe/emit/CNPJ").text
    print(cnpj_fornecedor)

    nome_destinatario = root.find("infNFe/dest/xNome").text
    print(nome_destinatario)

    descricao_produto = root.find("infNFe/det/prod/xProd").text
    print(descricao_produto)

    valor_produto = root.find("infNFe/det/prod/vProd").text
    print(valor_produto)

    valor_total = root.find("infNFe/total/ICMSTot/vNF").text
    print(valor_total)

    notas.append({
    "Numero": numero,
    "Data": data,
    "Fornecedor": nome_fornecedor,
    "CNPJ": cnpj_fornecedor,
    "Destinatário": nome_destinatario,
    "Descrição": descricao_produto,
    "Valor do Produto": valor_produto,
    "Total": valor_total,
})

import pandas as pd
df = pd.DataFrame(notas)
df.to_excel("notas_extraidas.xlsx", index=False)
