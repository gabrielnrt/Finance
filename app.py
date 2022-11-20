from dash import Dash, html, dcc, Input, Output
from plotly.express import line
from pandas import DataFrame, read_csv

import entrada
import processamento

carteira = entrada.leitura('CarteiraTeste.csv')

df = processamento.GeracaoTabela(carteira)
#
# df = read_csv('tabelafinal.csv')

lista = list(df['Nome'].unique())

# ISSO APARECE DUAS VEZES: UMA NO COMEÇO E OUTRA NO FIM
#print('oi')

app = Dash(__name__)
server = app.server

app.layout = html.Div(children = [
                html.H1('Análise Exploratória de uma carteira', style = {'textAlign':'center'}),

                html.Div('Selecione um ativo'),

                html.Br(),

                dcc.Dropdown(id = 'botao',
                             options = lista,
                             value = 'Carteira'),

                html.Br(),

                html.H1('Variações nos últimos 10 dias'),

                html.Table(id = 'tabela',
                           children = []),

                dcc.Graph(id = 'graficoAbs',
                          figure = {}),

                html.Br(),

                dcc.Graph(id = 'graficoPct',
                          figure = {})

])

@app.callback(
    [Output('graficoAbs', 'figure'), Output('graficoPct', 'figure'), Output('tabela', 'children')],
    Input('botao', 'value')
)
def FuncaoAtualizadora(ativo):

    sub_df = df.loc[ df['Nome'] == ativo ]

    figuraAbs = line(data_frame = sub_df,
                     x = 'Date',
                     y = 'Variação Total (R$)')

    figuraPct = line(data_frame = sub_df,
                     x = 'Date',
                     y = 'Variação Percentual')

    sub_df2 = sub_df.tail(10).copy()
    sub_df2['Date'] = sub_df2['Date'].apply(lambda x: x.strftime('%d/%m/%Y'))

    listaa = [
                html.Thead( html.Tr([html.Th(col) for col in sub_df2.columns])),
                html.Tbody([
                    html.Tr([
                        html.Td(sub_df2.iloc[i][col]) for col in sub_df2.columns
                    ]) for i in range(min(len(sub_df2), 10))
                ], style = {'textAlign':'center'})
            ]

    return figuraAbs, figuraPct, listaa

if __name__ == '__main__':
    app.run_server(debug = True)

# app.run_server(debug = True)
