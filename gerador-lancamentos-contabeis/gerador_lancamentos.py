"""
Gerador de Lançamentos Contábeis a partir de uma planilha de despesas.

Lê `despesas.xlsx` (Data, Fornecedor, Categoria, Valor) e
`plano_contas.xlsx` (Categoria, Conta), e gera `lancamentos_gerados.xlsx`
com débito/crédito em partida dobrada.
"""

import pandas as pd

ARQUIVO_DESPESAS = "despesas.xlsx"
ARQUIVO_PLANO_CONTAS = "plano_contas.xlsx"
ARQUIVO_SAIDA = "lancamentos_gerados.xlsx"
CONTA_CREDITO_PADRAO = "1.1.2 - Bancos Conta Movimento"
CONTA_NAO_CLASSIFICADA = "9.9.9 - A CLASSIFICAR (revisar manualmente)"


def carregar_despesas(caminho):
    df = pd.read_excel(caminho)
    colunas_esperadas = {"Data", "Fornecedor", "Categoria", "Valor"}
    faltando = colunas_esperadas - set(df.columns)
    if faltando:
        raise ValueError(f"Colunas faltando em '{caminho}': {faltando}")
    return df


def carregar_plano_de_contas(caminho):
    """Lê o plano de contas de uma planilha (Categoria -> Conta) e
    devolve como dicionário, pra não precisar editar o código Python
    toda vez que uma conta nova for cadastrada."""
    df = pd.read_excel(caminho)
    colunas_esperadas = {"Categoria", "Conta"}
    faltando = colunas_esperadas - set(df.columns)
    if faltando:
        raise ValueError(f"Colunas faltando em '{caminho}': {faltando}")
    return dict(zip(df["Categoria"], df["Conta"]))


def classificar_conta(categoria, plano_de_contas):
    return plano_de_contas.get(categoria, CONTA_NAO_CLASSIFICADA)


def gerar_lancamentos(despesas, plano_de_contas):
    linhas = []
    for _, despesa in despesas.iterrows():
        conta_debito = classificar_conta(despesa["Categoria"], plano_de_contas)
        linhas.append({
            "Data": despesa["Data"],
            "Histórico": f"{despesa['Categoria']} - {despesa['Fornecedor']}",
            "Conta Débito": conta_debito,
            "Conta Crédito": CONTA_CREDITO_PADRAO,
            "Valor": despesa["Valor"],
            "Precisa Revisão": conta_debito == CONTA_NAO_CLASSIFICADA,
        })
    return pd.DataFrame(linhas)


def validar_partida_dobrada(lancamentos):
    total_debito = lancamentos["Valor"].sum()
    total_credito = lancamentos["Valor"].sum()
    diferenca = round(total_debito - total_credito, 2)
    if diferenca != 0:
        raise ValueError(f"Partida dobrada não fecha! Diferença: R$ {diferenca}")
    return total_debito


def main():
    plano_de_contas = carregar_plano_de_contas(ARQUIVO_PLANO_CONTAS)
    despesas = carregar_despesas(ARQUIVO_DESPESAS)
    lancamentos = gerar_lancamentos(despesas, plano_de_contas)

    total = validar_partida_dobrada(lancamentos)
    pendentes = lancamentos["Precisa Revisão"].sum()

    lancamentos.to_excel(ARQUIVO_SAIDA, index=False)

    print(f"{len(lancamentos)} lançamentos gerados em '{ARQUIVO_SAIDA}'.")
    print(f"Total lançado: R$ {total:,.2f}")
    if pendentes:
        print(f"ATENÇÃO: {pendentes} lançamento(s) caíram em 'A CLASSIFICAR' — revisar categoria na planilha de entrada ou cadastrar no plano de contas.")
    else:
        print("Todas as despesas foram classificadas automaticamente.")


if __name__ == "__main__":
    main()
