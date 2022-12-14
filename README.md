# **Finance**

## **Objetivo**

  Neste repositório se encontra o projeto em que realizo uma análise exploratória de uma carteira de ativos com o objetivo de produzir um painel interativo que mostre gráficos das variações percentual e total, seguido de uma tabela contendo esses valores nos últimos 10 dias. O deploy foi feito no Heroku, e pode ser acessado neste link: http://carteirateste1.herokuapp.com/.

 <!-- em que o resultado é uma série de gráficos contendo a variação absoluta e percentual de cada ativo que compõe a carteira. No fim, também produzo um gráfico referente à essas variações da carteira como um todo. Para obter o histórico dos preços dos ativos, usei a biblioteca `pandas_datareader`.  -->



## **Arquivos**

  Segue abaixo uma breve descrição dos arquivos contidos usados:

### `Calculos.ipynb`

  Aqui eu essencialmente faço as demonstrações de como calcular a variação total e percentual de uma carteira contendo diferentes ativos.

### `AnaliseCarteira.ipynb`

  É neste notebook que desenvolvo passo a passo do primeiro bloco do projeto e a linha de raciocínio na produção dos gráficos das variações percentuais e absolutas de cada ativo, cobrindo desde o arquivo de entrada, passando por requisições API do [Yahoo Finance](https://br.financas.yahoo.com/), até chegar na geração dos gráficos propriamente ditos. No fim, produzo um arquivo contendo todo o histórico das variações de cada ativo, que é o ponto de partida para o painel interativo no notebook `Dashboard.ipynb`.

### `ScriptAnaliseCarteira.py`

  Este arquivo é o script contendo todas as linhas de comando em Python para a realização do projeto, pronto para ser executado no terminal ou em outra plataforma. A diferença deste arquivo com o anterior é que aqui eu não coloquei a explicação detalhada dos comandos (exceto em algumas partes), é mais o código em si de maneira enxuta e organizada na forma "Importação das Bibliotecas / Leitura dos dados iniciais / Processamento de Dados / Resultados".

### `CarteiraTeste.csv`

  Esta é a carteira fictícia usada como teste para geração de códigos, contendo o histórico das ordens efetuadas pelo investidor. Suas colunas são as seguintes:

  * Ativo: Ticker do ativo negociado na B3

  * Quantidade: Número de vezes que o mesmo ativo foi comprado no dia

  * Compra (R$): Valor da unidade do ativo no momento em que este foi comprado

  * Data da Compra: Dia em que o ativo foi comprado no formato `%d/%m/%Y`.

  Note que, por ser um histórico de ordens, então o mesmo ativo pode aparecer em linhas diferentes, com preços de compra e quantidades distintas, se o investidor fizer essas compras em momentos diferentes.

  Os ativos que compõem essa carteira são ITUB4, VALE3 e PETR4. **AVISO LEGAL: essas ações são meramente ilustrativas e de nenhuma forma representam recomendações de compra.**

### `tabelafinal.csv`

  Este arquivo é uma tabela do tipo `.csv` que possui o histórico das variações desde o dia da primeira compra de cada ativo. Eles estão concatenados e seguem uma ordem alfabética com relação ao ticker do ativo. No fim, há também o histórico da carteira como um todo.


### `Dashboard.ipynb`

  Este é o segundo bloco do projeto, onde desenvolvo o painel interativo. Para tal, uso as bibliotecas `dash` para a estrura do painel incluindo callbacks, `plotly.express` para a realização dos gráficos, e o `pandas` para leitura dos dados do arquivo `tabelafinal.csv`.

### `painel.py`

  Aqui eu coloquei num script todo o código desenvolvido no arquivo `Dashboard.ipynb`. Ao ser executado, ele produzirá um link de acesso que contém o Dashboard com os gráficos e as tabelas mencionadas anteriormente.

### Demais Arquivos

  Os demais arquivos - `Procfile`, `requirements.txt`, `entrada.py`, `processamento.py`, `app.py` - são relativos ao deploy do modelo feito com o auxílio da biblioteca `dash`.
