# **Finance**

## **Objetivo**

Neste repositório se encontra o projeto em que realizo uma análise exploratória de uma carteira de ativos, em que o resultado é uma série de gráficos contendo a variação absoluta e percentual de cada ativo que compõe a carteira. No fim, também produzo um gráfico referente à essas variações da carteira como um todo. Para obter o histórico dos preços dos ativos, usei a biblioteca `pandas_datareader`.


## **Arquivos**

Segue abaixo uma breve descrição dos arquivos contidos usados:

### `AnaliseCarteira.ipynb`

É neste notebook que desenvolvo passo a passo todo o projeto e a linha de raciocínio na produção dos gráficos das variações percentuais e absolutas de cada ativo, cobrindo desde o arquivo de entrada, passando por requisições API do [Yahoo Finance](https://br.financas.yahoo.com/), até chegar na geração dos gráficos propriamente ditos.

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

## **Cálculos**

### Definições básicas e generalizações

Definimos a **variação total** de um investimento por

$$ \Delta (t) \equiv A(t) - I(t),$$

onde $A(t)$ é o valor atual do patrimônio em $t$, e $I(t)$ é o valor investido até $t$.

Além disso, definimos a **variação percentual** como

$$ \delta (t) \equiv \frac{A(t) - I(t)}{I(t)} = \frac{A(t)}{I(t)} -1.$$

Essas são as ideias básicas para cumprir o objetivo deste projeto. Feito isso, vamos começar pelo exemplo mais simples e sofisticando-o aos poucos.

### Ex.1: $q_0$ unidades de um ativo comprados pelo preço (da unidade) $X_0$ em $t_0$

Como $I(t < t_0) = 0$, então não faz sentido fazer um gráfico para $t < t_0$. Daí, para $t > t_0$, $A(t) = q_0 X$, e $I(t) = q_0 X_0$, onde $X = X(t)$ é o preço do ativo em $t$; o que nos leva a

$$  \Delta (t) = q_0(X - X_0), $$

$$ \delta (t) = \frac{X}{X_0} -1. $$

### Ex.2: Um mesmo ativo comprado em 2 instantes distintos

Sejam $q_1 = q(t_1)$ e $X_1 = X(t_1)$, com $t_1 > t_0$, e $(q_0,X_0)$ como no exemplo anterior. Logo, para $t_0 < t < t_1$ a variação total continua sendo $\Delta = q_0(X - X_0)$; mas, para $t > t_1$, temos $A(t) = q_0X + q_1X = (q_0 + q_1)X$ e $I(t) = q_0X_0 + q_1X_1$; e assim, definindo a quantidade total $Q$ como

$$ Q \equiv q_0 + q_1,$$

e chamando a média ponderada do preço do ativo comprado nos instantes $t_0$ e $t_1$ de $ \overline{X} $,

$$ \overline{X} \equiv \frac{q_0 X_0 + q_1 X_1}{q_0 + q_1}, $$

segue que

$$ \Delta = (q_0 + q_1)X - (q_0X_0 + q_1X_1)  = Q(X - \overline{X}),$$

$$ \delta = \frac{(q_0 + q_1)X}{q_0 X_0 + q_1 X_1} -1 = \frac{X}{\overline{X}} -1.$$

Portanto,

$$
\Delta (t) =
\begin{cases}
q_0(X - X_0) & t_0 < t < t_1, \\
Q(X - \overline{X}) & t_1 < t.
\end{cases}  
$$

$$ \delta (t) = \begin{cases} X X_0^{-1} -1 & t_0 < t < t_1, \\ X \overline{X}^{-1} -1 & t_1 < t. \end{cases} $$

### Ex.3: Um mesmo ativo comprado em $n$ instantes distintos

Fazendo $n$ compras de um mesmo ativo em instantes distintos, é fácil mostrar que as variações terão a mesma estrutura que no caso anterior.

Chamando a quantidade total até a k-ésima compra ($k < n$) por

$$ Q_k \equiv \sum_{i = 0}^k q_i,$$

e a média ponderada até a k-ésima compra por

$$ \overline{X}_k \equiv \frac{1}{Q_k} \sum_{i = 0}^k q_i X_i, $$

segue que a variação total é

$$
\Delta (t) =
\begin{cases}
 q_0(X - X_0) & t_0 < t < t_1, \\
 \vdots \\
 Q_k(X - \overline{X}_k) & t_k < t < t_{k+1}, \\
 \vdots \\
 Q_{n-1}(X - \overline{X}_{n-1}) & t_{n-1} < t,
 \end{cases}
$$

e que a variação percentual é

$$ \delta (t) = \begin{cases} X(X_0)^{-1} -1 & t_0 < t < t_1, \\ \vdots \\ X(\overline{X}_k)^{-1} -1 & t_k < t < t_{k+1}, \\ \vdots \\ X(\overline{X}_{n-1})^{-1} -1 & t_{n-1} < t. \end{cases} $$
