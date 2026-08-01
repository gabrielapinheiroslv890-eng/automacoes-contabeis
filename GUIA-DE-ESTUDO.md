# Guia de Estudo — Portfólio de Automações Contábeis

> Documento pra você estudar antes de uma apresentação ou entrevista. Não é só uma lista técnica — é pra você conseguir explicar cada projeto com naturalidade, incluindo os erros que apareceram no caminho (isso conta a favor, não contra: mostra processo real de trabalho).

**Repositório**: https://github.com/gabrielapinheiroslv890-eng/automacoes-contabeis

---

## Como usar esse documento

Pra cada projeto, tem 5 blocos:
- **O que é, em uma frase** — a resposta rápida se alguém perguntar "me conta um projeto seu"
- **O problema real** — por que isso importa na contabilidade, não só "o que o código faz"
- **Como funciona por dentro** — a lógica, explicada sem jargão técnico desnecessário
- **Os erros que apareceram (e por quê)** — sua munição mais forte numa entrevista
- **Se perguntarem "e se..."** — respostas prontas pra perguntas de aprofundamento comuns

**Dica geral de apresentação**: não comece pelo código. Comece pelo problema ("na contabilidade, conferir extrato bancário manualmente demora X e erra Y"), depois mostre a solução funcionando (print ou demo ao vivo), só depois entre em detalhe técnico se perguntarem. Ninguém quer ver código antes de entender por que ele existe.

---

## Projeto 1 — Conciliação Bancária Automática

**O que é, em uma frase**: um script no Google Sheets que compara automaticamente o extrato do banco com os lançamentos já registrados, apontando o que bate e o que não bate.

### O problema real
Toda empresa precisa conferir, periodicamente, se o que está registrado nos livros bate com o que realmente passou pelo banco. Feito à mão, isso é olhar linha por linha em duas listas — lento e você erra fácil quando tem muita linha parecida.

### Como funciona por dentro
O script pega cada linha do extrato e procura, na lista de lançamentos, uma linha com **valor idêntico** e **data próxima** (até 2 dias de diferença, porque banco às vezes compensa depois). Quando duas linhas empatam nesse critério (mesma data, mesmo valor — comum quando várias pessoas pagam o mesmo valor no mesmo dia), o script desempata olhando se as **palavras da descrição** batem (ex: o nome de um aluno aparece nos dois lados).

Se você for explicar isso numa entrevista, a frase-chave é: *"o script não pega o primeiro candidato que aparece, ele calcula qual é o melhor candidato, considerando data e texto da descrição."* Isso mostra que você pensou em qualidade do resultado, não só em "fazer funcionar".

### Os erros que apareceram (e por quê)
1. **TypeError ao rodar**: o código ficou incompleto depois de colar errado no editor — ensinou a sempre limpar o editor por completo antes de colar código novo, em vez de confiar que a colagem por cima vai substituir tudo certo.
2. **Pareamento errado**: a primeira versão pegava sempre o primeiro lançamento que batesse em valor e data — então quando dois alunos pagavam o mesmo valor no mesmo dia, o script "roubava" o par errado. Descoberto testando com dados propositalmente ambíguos (dois alunos, mesmo valor, datas próximas) — e resolvido comparando a descrição como critério de desempate.

### Se perguntarem "e se..."
- *"E se o extrato tiver 10 mil linhas?"* — o Google Sheets/Apps Script aguenta, mas ficaria lento. Pra escala maior, migraria isso pra Python.
- *"Por que não usar IA/machine learning pra isso?"* — pra esse volume e esse tipo de regra (data + valor + texto), um algoritmo determinístico é mais previsível e mais fácil de auditar do que um modelo de ML — importante em contabilidade, onde você precisa conseguir explicar por que um lançamento foi classificado de um jeito.

---

## Projeto 2 — Gerador de Lançamentos Contábeis (Python)

**O que é, em uma frase**: um script Python que lê uma planilha de despesas e gera os lançamentos contábeis (débito e crédito) automaticamente, respeitando o princípio da partida dobrada.

### O problema real
Lançar despesa por despesa, decidindo manualmente qual conta contábil usar pra cada categoria, é repetitivo e sujeito a erro de classificação — principalmente quando o volume é alto.

### Como funciona por dentro
Existe um "plano de contas" — um de-para de categoria (ex: "Aluguel") pra conta contábil (ex: "4.1.2 - Aluguel e Condomínio"). O script lê cada despesa, olha a categoria, busca a conta correspondente nesse de-para, e monta o lançamento (débito na conta da despesa, crédito numa conta bancária). No final, ele **valida**: soma de todos os débitos tem que ser igual à soma de todos os créditos — é o princípio contábil da partida dobrada, verificado em código.

Ponto importante pra explicar: o plano de contas **não fica fixo no código**, fica numa planilha separada. Isso significa que alguém sem saber programar consegue cadastrar uma conta nova, só editando o Excel.

### Os erros que apareceram (e por quê)
- Não teve bug de execução propriamente — a "evolução" desse projeto foi arquitetural: a primeira versão tinha o plano de contas dentro do próprio código Python (um dicionário fixo). Perceber que isso limitava quem pudesse manter o sistema levou à decisão de mover pra planilha externa.

### Se perguntarem "e se..."
- *"E se a categoria não estiver cadastrada?"* — o script não trava nem inventa uma conta: marca como "A CLASSIFICAR" e sinaliza no relatório final, pra alguém revisar manualmente. Nunca lança errado silenciosamente.
- *"Por que validar a partida dobrada, se cada linha já nasce balanceada?"* — é uma rede de segurança: se algum dia a lógica mudar (por exemplo, dividir uma despesa em duas contas), essa validação pega erro antes de exportar.

---

## Projeto 3 — Dashboard de Apuração de Impostos (Simples Nacional)

**O que é, em uma frase**: cálculo automático do Simples Nacional mês a mês (considerando a receita acumulada, não só o faturamento do mês), visualizado num dashboard Power BI.

### O problema real
O Simples Nacional não usa uma alíquota fixa — ela **sobe** conforme a receita acumulada dos últimos 12 meses cresce. Fazer essa conta certa manualmente, mês após mês, é fácil de errar.

### Como funciona por dentro
A fórmula oficial: `Alíquota Efetiva = (RBT12 × Alíquota Nominal − Valor a Deduzir) / RBT12`, onde RBT12 é a receita acumulada. O script Python calcula essa receita acumulada, identifica em qual "faixa" a empresa está (usando uma tabela oficial de faixas), aplica a fórmula, e o Power BI mostra a evolução — inclusive um gráfico colorido que mostra visualmente quando a empresa "sobe de faixa".

### Os erros que apareceram (e por quê) — esse é o mais rico dos 7
A primeira tentativa foi calcular tudo **dentro do Power BI**, usando colunas DAX com `CALCULATE`. Isso gerou um erro de **dependência circular** que persistiu mesmo depois de várias tentativas de correção — inclusive resíduos de estado corrompido entre sessões do Power BI Desktop. A decisão final foi: mover **todo o cálculo pra Python**, deixando o Power BI responsável só pela visualização.

Essa é a história mais forte do portfólio inteiro pra contar numa entrevista, porque mostra: (1) você tentou resolver no lugar "certo" primeiro, (2) você identificou que o problema não era pontual, era estrutural, (3) você tomou uma decisão de arquitetura (separar cálculo de visualização) em vez de insistir infinitamente na mesma abordagem.

**Frase pronta pra entrevista**: *"Eu descobri na prática uma diferença importante do DAX: usar CALCULATE dentro de uma coluna calculada tenta travar a linha inteira da tabela, incluindo a própria coluna que está sendo calculada — isso cria um ciclo. Depois de confirmar que o problema era estrutural, decidi separar responsabilidades: Python calcula, Power BI só mostra."*

### Se perguntarem "e se..."
- *"Você resolveria isso com medida DAX em vez de coluna?"* — sim, e de fato no Projeto 6 isso foi confirmado: a mesma lógica de soma condicional funcionou sem problema nenhum quando escrita como **medida** em vez de coluna calculada, porque medida não faz a "transição de contexto" que trava a linha inteira.
- *"Por que não corrigir o DAX até funcionar, por teimosia?"* — porque em ambiente de trabalho real, tempo importa. Reconhecer quando trocar de abordagem é mais rápido que insistir é uma habilidade, não uma desistência.

---

## Projeto 4 — Leitor de Extrato Bancário em PDF

**O que é, em uma frase**: script Python que extrai transações direto de um PDF de extrato bancário (sem digitação manual), lidando com formatos de valor diferentes usados por bancos diferentes.

### O problema real
Nem todo extrato vem em Excel pronto — muito banco só exporta PDF. Copiar isso manualmente é lento e sujeito a erro de digitação.

### Como funciona por dentro
Usa uma biblioteca (`pdfplumber`) pra extrair o texto puro do PDF, depois um **padrão de reconhecimento de texto** (regex) pra achar linhas no formato "data + descrição + valor". A parte mais interessante: o "leitor de valor" foi desenhado pra entender vários formatos que bancos diferentes usam — `450,00`, `-35,90`, `R$ 450,00`, `(35,90)` (negativo entre parênteses), `35,90 D` (D de débito, em vez de sinal de menos).

### Os erros que apareceram (e por quê)
Não teve bug de execução — o "erro" evitado aqui foi de **design**: a primeira versão só reconhecia um formato de valor. Antes de considerar pronto, foi feito um segundo PDF de teste, simulando um banco com formato **diferente** (R$, parênteses, sufixo D/C), especificamente pra provar que a solução generaliza — e não foi só ajustada pro primeiro caso que apareceu.

### Se perguntarem "e se..."
- *"E se o PDF for escaneado (imagem), não texto?"* — não funcionaria assim; precisaria de OCR (reconhecimento óptico de caractere, tipo Tesseract), que não foi implementado. Essa é uma limitação conhecida e documentada, não escondida.
- *"Por que regex e não IA pra extrair o texto?"* — porque o formato é bem estruturado (data, descrição, valor sempre nessa ordem). Regex é mais rápido, mais previsível e mais fácil de debugar que uma solução de IA pra esse caso específico.

---

## Projeto 5 — App de Geração de Lançamentos (Streamlit)

**O que é, em uma frase**: a mesma lógica do Projeto 2, só que com uma interface web — upload de arquivo, botão, tabela de resultado, download — em vez de terminal.

### O problema real
Um script de terminal só serve pra quem sabe programar. Uma interface web abre a ferramenta pra qualquer pessoa da equipe usar.

### Como funciona por dentro
Streamlit é um framework que transforma um script Python comum numa página web, sem precisar saber HTML/CSS/JavaScript. O app recebe 3 arquivos por upload (despesas, plano de contas, formas de pagamento), reprocessa a mesma lógica de negócio do Projeto 2, e mostra o resultado em cards visuais e numa tabela colorida.

O incremento mais importante em cima do Projeto 2: **conta de crédito variável por forma de pagamento** — em vez de sempre creditar a mesma conta bancária, cada despesa credita a conta certa conforme foi paga em PIX, Cartão ou Boleto.

### Os erros que apareceram (e por quê) — 4 no total, bom material
1. **Variável com nome de função**: nomeou uma variável igual a uma função já existente (`carregar_planilha`), fazendo o Python "esquecer" que aquilo era uma função depois dali.
2. **Import misturado com código**: uma linha de interface (`st.file_uploader`) colou por cima do `import pandas as pd`, quebrando os dois.
3. **Chamada de carregamento esquecida**: tentou usar uma variável (`forma_pagamento_df`) sem antes criar ela — faltava a linha que efetivamente lê o arquivo.
4. **KeyError por arquivo desatualizado**: o app rodava sem erro, mas a coluna nova não existia porque o arquivo enviado pelo upload era uma versão antiga.

**Frase pronta**: *"Cada um desses erros me ensinou uma distinção fundamental de Python: nome de variável vs. nome de função, aspas (texto literal) vs. sem aspas (valor de variável), e a importância de garantir que uma variável existe antes de usar ela."*

### Se perguntarem "e se..."
- *"Por que não usar Flask/Django em vez de Streamlit?"* — Streamlit é feito pra prototipagem rápida de ferramentas internas, com muito menos código. Flask/Django fazem mais sentido pra um produto com autenticação de usuário, banco de dados, etc. — overkill pra esse caso.
- *"O Excel é salvo no servidor?"* — não, é gerado em memória (`io.BytesIO`) e entregue direto pro navegador — importante se o app um dia rodar hospedado, onde talvez não haja permissão de escrita em disco.

---

## Projeto 6 — Painel Financeiro (Contas a Pagar/Receber) — Power BI Avançado

**O que é, em uma frase**: um dashboard Power BI com modelo de dados relacional de verdade (5 tabelas conectadas), calculando o saldo entre o que a empresa paga e recebe.

### O problema real
Contas a pagar e a receber vêm de fontes diferentes (fornecedores, clientes). Pra enxergar o saldo líquido do período, você precisa cruzar essas fontes — o que fica bagunçado numa planilha única cheia de PROCV.

### Como funciona por dentro
Um **modelo em esquema estrela**: duas tabelas de "fato" (Contas a Pagar, Contas a Receber) ligadas a três tabelas de "dimensão" (Fornecedores, Clientes, Calendário). Três medidas DAX calculam Total Pago, Total Recebido e o Saldo (a diferença entre os dois).

Esse projeto foi construído com bem mais autonomia que os anteriores — a maior parte (relacionamentos, medidas) foi escrita sem apoio direto, só com verificação depois.

### Os erros que apareceram (e por quê)
Interessante que esse projeto **não teve** o bug de dependência circular do Projeto 3 — porque dessa vez, a lógica de soma condicional foi escrita como **medida**, não como coluna calculada. Isso confirma, na prática, a lição aprendida no Projeto 3.

**Frase pronta**: *"Regra que aprendi na prática: quando você precisa de uma soma agregada condicional, usa medida. Quando precisa de um valor calculado linha a linha que vai aparecer numa tabela, aí sim considera coluna — com cuidado, porque CALCULATE dentro de coluna pode dar o mesmo problema que tive no Projeto 3."*

### Se perguntarem "e se..."
- *"Por que esquema estrela e não uma tabela única?"* — porque cada fornecedor pode ter várias contas a pagar, e cada cliente várias contas a receber — juntar tudo numa tabela só duplicaria dados e dificultaria manutenção. É o padrão usado em qualquer ferramenta de BI de mercado.
- *"Como você confirmou que os relacionamentos estavam certos?"* — não confiando só no diagrama visual (que fica confuso com várias tabelas conectadas) — usando a lista de texto em "Gerenciar relações", que mostra exatamente "Tabela A.Coluna → Tabela B.Coluna" sem ambiguidade.

---

## Projeto 7 — Leitor de XML de Nota Fiscal Eletrônica (NF-e)

**O que é, em uma frase**: script Python que lê o arquivo XML oficial de uma nota fiscal eletrônica e extrai os dados principais automaticamente.

### O problema real
Toda NF-e emitida no Brasil gera um XML oficial (não PDF, não Excel). Conferir nota por nota manualmente é inviável em volume — e esse é um dos formatos mais comuns de automação real em controladoria.

### Como funciona por dentro
Usa a biblioteca nativa do Python pra XML (`xml.etree.ElementTree`, não precisa instalar nada) pra navegar pela estrutura de tags aninhadas do XML (`infNFe → emit → xNome`, por exemplo) e extrair número, data, fornecedor, CNPJ, produto e valores. Um laço processa **todos** os arquivos XML de uma pasta automaticamente, consolidando numa única planilha.

Esse foi o projeto mais "aprendido na prática" — a lógica foi construída campo por campo, arquivo por arquivo, com bastante autonomia.

### Os erros que apareceram (e por quê) — 4, muito didáticos
1. **Confundir "abrir visualmente" com "ler via código"** — no início não estava claro que o Python lê um arquivo pelo **nome**, como texto, sem precisar "abrir" ele numa aba pra visualizar.
2. **Aspas em volta de uma variável** — `ET.parse("arquivo")` com aspas tenta abrir um arquivo chamado literalmente "arquivo", em vez de usar o valor da variável `arquivo` do loop.
3. **Copiar/colar sem atualizar o caminho** — ao duplicar a linha de um campo pra criar outro, o caminho dentro do `.find()` não foi trocado, então várias variáveis acabaram lendo o mesmo dado.
4. **Código fora da indentação do loop** — as linhas de extração ficaram "fora" do `for`, rodando só uma vez em vez de uma vez por arquivo.

**Frase pronta**: *"Esse foi o projeto onde mais aprendi fazendo — cada erro me ensinou uma regra fundamental de Python: a diferença entre string literal e variável, a importância da indentação pra definir o que está 'dentro' de um loop, e como ler a estrutura de um arquivo de dados direto na fonte, em vez de confiar só numa explicação de fora."*

### Se perguntarem "e se..."
- *"E se a nota tiver mais de um produto?"* — a versão atual só pega o primeiro item (`det`); é uma limitação conhecida, documentada como próximo incremento.
- *"Você decorou os caminhos das tags XML?"* — não, abriu o XML direto no editor de código e leu a estrutura real, contando os níveis de aninhamento — é assim que se descobre o caminho certo em qualquer XML novo, não só nesse exemplo.

---

## Perguntas gerais que podem aparecer (sobre o portfólio como um todo)

**"Por que você usou tantas ferramentas diferentes (Apps Script, Python, Power BI, Streamlit)?"**
Porque cada rotina contábil real pede uma ferramenta diferente: Google Sheets/Apps Script quando o time já trabalha em planilha colaborativa; Python quando a lógica é mais pesada ou envolve arquivo (PDF, XML); Power BI quando o objetivo é visualização executiva; Streamlit quando a ferramenta precisa ser usável por quem não programa. Escolher a ferramenta certa pro problema, não a ferramenta favorita, é parte da competência.

**"Qual desses você tem mais orgulho?"**
Resposta honesta e pessoal — mas se quiser um argumento pronto: o Projeto 3 (Apuração de Impostos) pela decisão técnica de trocar de abordagem, ou o Projeto 7 (NF-e) pelo processo de aprendizado mais hands-on.

**"O que você faria diferente se recomeçasse?"**
Boa chance de mencionar: testar com dados propositalmente ambíguos desde o início (como foi feito no Projeto 1, mas poderia ter sido a prática padrão em todos desde o começo).

**"Isso é só protótipo ou você usaria em produção?"**
Honestidade: são protótipos de portfólio, com dados fictícios — mas a lógica de negócio (partida dobrada, cálculo de impostos, formato NF-e) é real. Pra produção, precisaria de: tratamento de erro mais robusto, testes automatizados, e provavelmente autenticação/permissões se fosse multiusuário.

---

*Documento gerado em 31/07/2026, cobrindo os 7 projetos concluídos do portfólio. O Projeto 8 (Relatório Executivo Multipágina) está em andamento.*
