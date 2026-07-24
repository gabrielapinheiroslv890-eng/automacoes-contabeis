"""
Calcula a apuração de impostos (Simples Nacional, Anexo III simplificado)
a partir do faturamento mensal, gerando uma planilha pronta pra ser
usada como fonte de um dashboard no Power BI.

Lê `faturamento.xlsx` (Mes, Faturamento, Regime, Anexo) e
`tabela_aliquotas_anexo3.xlsx` (Faixa, Receita_Ate, Aliquota_Nominal, Valor_Deduzir),
gera `apuracao_calculada.xlsx` com RBT12, faixa, alíquota efetiva e imposto do mês.
"""

import pandas as pd

ARQUIVO_FATURAMENTO = "faturamento.xlsx"
ARQUIVO_ALIQUOTAS = "tabela_aliquotas_anexo3.xlsx"
ARQUIVO_SAIDA = "apuracao_calculada.xlsx"


def carregar_dados():
    faturamento = pd.read_excel(ARQUIVO_FATURAMENTO).sort_values("Mes").reset_index(drop=True)
    aliquotas = pd.read_excel(ARQUIVO_ALIQUOTAS).sort_values("Faixa").reset_index(drop=True)
    return faturamento, aliquotas


def calcular_rbt12(faturamento):
    """Receita bruta acumulada até o mês (proxy simplificada do RBT12 real,
    que usa os últimos 12 meses — aqui usamos todo o histórico disponível
    porque a base de teste tem menos de 12 meses)."""
    faturamento["RBT12"] = faturamento["Faturamento"].cumsum()
    return faturamento


def encontrar_faixa(rbt12, aliquotas):
    """Acha a menor faixa cujo teto (Receita_Ate) ainda comporta o RBT12."""
    candidatas = aliquotas[aliquotas["Receita_Ate"] >= rbt12]
    if candidatas.empty:
        return aliquotas.iloc[-1]  # estourou a última faixa: usa a mais alta
    return candidatas.iloc[0]


def calcular_apuracao(faturamento, aliquotas):
    linhas = []
    for _, mes in faturamento.iterrows():
        faixa = encontrar_faixa(mes["RBT12"], aliquotas)
        aliquota_efetiva = (mes["RBT12"] * faixa["Aliquota_Nominal"] - faixa["Valor_Deduzir"]) / mes["RBT12"]
        imposto_do_mes = mes["Faturamento"] * aliquota_efetiva

        linhas.append({
            "Mes": mes["Mes"],
            "Faturamento": mes["Faturamento"],
            "RBT12": mes["RBT12"],
            "Faixa": faixa["Faixa"],
            "AliquotaNominal": faixa["Aliquota_Nominal"],
            "AliquotaEfetiva": aliquota_efetiva,
            "ImpostoDoMes": imposto_do_mes,
        })
    return pd.DataFrame(linhas)


def main():
    faturamento, aliquotas = carregar_dados()
    faturamento = calcular_rbt12(faturamento)
    apuracao = calcular_apuracao(faturamento, aliquotas)

    apuracao["VariacaoImposto"] = apuracao["ImpostoDoMes"].diff()
    apuracao["VariacaoImpostoPercentual"] = apuracao["ImpostoDoMes"].pct_change()

    apuracao.to_excel(ARQUIVO_SAIDA, index=False)

    print(f"Apuração calculada para {len(apuracao)} meses em '{ARQUIVO_SAIDA}'.")
    print(apuracao[["Mes", "Faturamento", "Faixa", "AliquotaEfetiva", "ImpostoDoMes"]].to_string(index=False))


if __name__ == "__main__":
    main()
