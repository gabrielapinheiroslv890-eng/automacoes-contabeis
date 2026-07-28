"""
Interface web (Streamlit) pro Gerador de Lançamentos Contábeis.

Mesma lógica do projeto 2 (débito/crédito por categoria, validação de
partida dobrada), agora com upload de arquivo pela interface em vez de
nomes de arquivo fixos, e resultado exibido/baixável direto na tela.
"""

import io

import pandas as pd
import streamlit as st

CONTA_CREDITO_PADRAO = "1.1.2 - Bancos Conta Movimento"
CONTA_NAO_CLASSIFICADA = "9.9.9 - A CLASSIFICAR (revisar manualmente)"


def carregar_planilha(arquivo, colunas_esperadas):
    df = pd.read_excel(arquivo)
    faltando = colunas_esperadas - set(df.columns)
    if faltando:
        raise ValueError(f"Colunas faltando: {faltando}")
    return df


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


def gerar_excel_para_download(lancamentos):
    buffer = io.BytesIO()
    lancamentos.to_excel(buffer, index=False)
    return buffer.getvalue()


def main():
    st.set_page_config(page_title="Gerador de Lançamentos Contábeis", page_icon="📒")
    st.title("📒 Gerador de Lançamentos Contábeis")
    st.caption("Envie a planilha de despesas e o plano de contas — o app gera os lançamentos automaticamente.")

    col1, col2 = st.columns(2)
    with col1:
        arquivo_despesas = st.file_uploader("Planilha de Despesas (.xlsx)", type="xlsx")
    with col2:
        arquivo_plano = st.file_uploader("Plano de Contas (.xlsx)", type="xlsx")

    if not (arquivo_despesas and arquivo_plano):
        st.info("Envie os dois arquivos pra continuar.")
        return

    try:
        despesas = carregar_planilha(arquivo_despesas, {"Data", "Fornecedor", "Categoria", "Valor"})
        plano_df = carregar_planilha(arquivo_plano, {"Categoria", "Conta"})
        plano_de_contas = dict(zip(plano_df["Categoria"], plano_df["Conta"]))
    except ValueError as erro:
        st.error(f"Erro ao ler os arquivos: {erro}")
        return

    lancamentos = gerar_lancamentos(despesas, plano_de_contas)
    total = lancamentos["Valor"].sum()
    pendentes = lancamentos["Precisa Revisão"].sum()

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Lançamentos gerados", len(lancamentos))
    col_b.metric("Total lançado", f"R$ {total:,.2f}")
    col_c.metric("Precisam revisão", int(pendentes), delta_color="inverse")

    if pendentes:
        st.warning(f"{pendentes} lançamento(s) caíram em 'A CLASSIFICAR' — cadastre a categoria no plano de contas ou revise manualmente.")
    else:
        st.success("Todas as despesas foram classificadas automaticamente.")

    def destacar_pendentes(linha):
        cor = "background-color: #fff2cc" if linha["Precisa Revisão"] else ""
        return [cor] * len(linha)

    st.dataframe(lancamentos.style.apply(destacar_pendentes, axis=1), use_container_width=True)

    excel_bytes = gerar_excel_para_download(lancamentos)
    st.download_button(
        "⬇️ Baixar lançamentos (.xlsx)",
        data=excel_bytes,
        file_name="lancamentos_gerados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    main()
