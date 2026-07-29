# App de Geração de Lançamentos Contábeis (Streamlit)

Interface web pro [Gerador de Lançamentos Contábeis](../gerador-lancamentos-contabeis) — mesma lógica de classificação e partida dobrada, agora acessível por upload de arquivo e visualização direto no navegador, sem precisar usar terminal.

## O problema

O Projeto 2 (versão em linha de comando) funciona bem, mas exige que quem for usar saiba rodar Python no terminal e edite os nomes de arquivo no código. Uma interface web torna a ferramenta usável por qualquer pessoa da equipe, sem conhecimento técnico.

## A solução

Um app Streamlit de página única que:

1. Recebe três arquivos por upload (despesas, plano de contas e formas de pagamento), em vez de nomes de arquivo fixos
2. Reaproveita a mesma lógica de classificação e validação de partida dobrada do Projeto 2
3. **Conta de crédito variável por forma de pagamento**: em vez de sempre creditar a mesma conta bancária, cada despesa credita a conta certa conforme a forma de pagamento (PIX → Bancos, Cartão → Cartão de Crédito a Pagar, Boleto → Fornecedores a Pagar) — configurável em planilha, no mesmo padrão do plano de contas
4. Mostra o resultado em cards de métrica (quantidade, total, pendências) e numa tabela com as linhas "a classificar" destacadas em amarelo
5. Gera o Excel de saída em memória (sem salvar nada no servidor) e oferece direto pra download

## Como usar

```bash
streamlit run app.py
