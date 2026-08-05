import pandas as pd

contas_receber = pd.read_excel("contas_receber.xlsx")
clientes = pd.read_excel("clientes.xlsx")
agrupado = contas_receber.groupby("ClienteID").agg(
    Total_Receber = ("Valor", "sum"),
    Quantidade_Titulos = ("ContaReceberID", "count")
).reset_index()
print(agrupado)

agrupado["Ticket_Medio"] = agrupado["Total_Receber"] / agrupado["Quantidade_Titulos"]
print(agrupado)

atrasados = contas_receber[contas_receber["Status"] == "Atrasado"]
atrasados = atrasados.groupby("ClienteID").agg(
    Atrasados=("ContaReceberID", "count")
).reset_index()

agrupado = agrupado.merge(
    atrasados,
    on="ClienteID",
    how="left" 
)

agrupado["Atrasados"] = agrupado["Atrasados"].fillna(0).astype(int)
print(agrupado)

agrupado["Pct_Inadimplencia"] = agrupado["Atrasados"]/ agrupado["Quantidade_Titulos"]

resultado = agrupado.merge(clientes, on="ClienteID", how="left")
resultado.to_excel("indicadores_clientes.xlsx", index=False)
print(resultado)