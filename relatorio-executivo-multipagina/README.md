# Relatório Executivo Multipágina (Python + Power BI)

Relatório financeiro com navegação entre páginas (estilo apresentação), combinando indicadores calculados em Python com um dashboard Power BI de 4 páginas conectadas por botões.

## O problema

Um dashboard de página única mistura informação de nível diferente (resumo executivo, detalhamento operacional) no mesmo espaço. Separar por página, com navegação guiada, deixa a apresentação mais clara pra públicos diferentes — quem quer só o resumo não precisa rolar por tabelas detalhadas.

## A solução

### Parte 1 — Python (`calcular_indicadores.py`)
Calcula dois indicadores por cliente que o Power BI sozinho não calcula com a mesma clareza:
- **Ticket médio**: total recebido ÷ quantidade de títulos
- **% de inadimplência**: títulos atrasados ÷ total de títulos

Usa `groupby().agg()` com agregação nomeada pra somar e contar ao mesmo tempo, um segundo agrupamento filtrado só pelos atrasados, e `merge(..., how="left")` pra juntar sem perder clientes sem atraso.

### Parte 2 — Power BI (4 páginas)
- **Resumo**: cartões com Total Pago, Total Recebido, Saldo do Período — a "capa" do relatório
- **Contas a Pagar**: detalhamento por fornecedor
- **Contas a Receber**: detalhamento por cliente, incluindo os indicadores calculados em Python (ticket médio, % inadimplência)
- **Evolução**: gráfico de linha comparando Total Pago vs. Total Recebido mês a mês

As páginas são conectadas por **botões de navegação** (Ação → Página → Destino), com ida do Resumo pra cada página de detalhe e volta de cada página pro Resumo — funciona como slides de apresentação, sem depender das abas de página ficarem visíveis.

## Como usar

```bash
python calcular_indicadores.py
