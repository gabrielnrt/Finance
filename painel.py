from dash import Dash, html, dcc, Input, Output
from plotly.express import line
from pandas import DataFrame, read_csv


df = read_csv('tabelafinal.csv')

lista = list(df['Nome'].unique())

app = Dash(__name__)

app.layout = html.Div(children = [
                html.H1('Análise Exploratória de uma carteira'),

                html.Div('Selecione um ativo'),

                html.Br(),

                dcc.Dropdown(id = 'botao',
                             options = lista,
                             value = 'Carteira'),

                dcc.Graph(id = 'graficoAbs',
                          figure = {}),

                html.Br(),

                dcc.Graph(id = 'graficoPct',
                          figure = {}),

                html.Br(),

                html.H1('Variações nos últimos 10 dias'),

                html.Table(id = 'tabela',
                           children = [])

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

    sub_df2 = sub_df.tail(10)

    listaa = [
                html.Thead( html.Tr([html.Th(col) for col in sub_df2.columns])),
                html.Tbody([
                    html.Tr([
                        html.Td(sub_df2.iloc[i][col]) for col in sub_df2.columns
                    ]) for i in range(min(len(sub_df2), 10))
                ])
            ]

    return figuraAbs, figuraPct, listaa

if __name__ == '__main__':
    app.run_server(debug = True)
