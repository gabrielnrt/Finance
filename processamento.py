#---------------------------------------------------------
# Importação das bibliotecas

from pandas import DataFrame, read_csv, concat
from datetime import datetime, date
from pandas_datareader import data as web
from numpy import average, zeros, array



#-----------------------------------------------------------
# Contantes

hoje = date.today()

#-----------------------------------------------------------
# Requisição API Yahoo

def yahoo(ativo,tabela):

    fechas = list( tabela['Data da Compra'] )

    PrimeiraCompra = fechas[0]

    cotacoes = web.DataReader(ativo + '.SA',
                              data_source = 'yahoo',
                              start = PrimeiraCompra,
                              end = hoje)

    return cotacoes

# Função que retorna uma lista que é a soma acumulada da lista de entrada

def Soma(subcarteira):
    lista_antiga = list(subcarteira['Quantidade'])

    lista_nova = []
    for indice in range(0, len(lista_antiga)):
        if indice == 0:
            lista_nova.append(lista_antiga[indice])
        else:
            lista_nova.append( lista_antiga[indice] + lista_nova[indice - 1] )

    return lista_nova

# Lista de médias ponderadas

def Media(subcarteira):
    resultado = []

    valores = list(subcarteira['Compra (R$)'])
    pesos = list(subcarteira['Quantidade'])

    v_parcial = []
    p_parcial = []

    for indice in range(0, len(valores)): # poderia ser len(pesos) também
        v_parcial.append(valores[indice])
        p_parcial.append(pesos[indice])

        media = average(a = v_parcial,
                        weights = p_parcial)

        resultado.append(media)

    return resultado

# Função que insere colunas de Q_k e X_k em df
def Copias(subcarteira, df):
    listaQ = []
    listaX = []

    q = list( subcarteira['Q_k'])
    x = list( subcarteira['X_k'])

    DataCompra = list( subcarteira['Data da Compra'])

    ultimoindice = len(DataCompra) - 1

    UltimaData = DataCompra[ ultimoindice ]

    indice = 0

    for dia in df.index:

        if dia >= UltimaData:

            listaQ.append(q[ultimoindice])
            listaX.append(x[ultimoindice])

        else:

            if dia >= DataCompra[indice] and dia < DataCompra[indice + 1]:

                listaQ.append(q[indice])
                listaX.append(x[indice])

            else:

                indice += 1
                listaQ.append(q[indice])
                listaX.append(x[indice])

    return listaQ, listaX


def GeracaoTabela(carteira):
    #-----------------------------------------------------------------------------------
    # Processamento de dados


    carteira.sort_values(by = 'Data da Compra',
                         inplace = True)

    lista = list( set(carteira['Ativo']) )

    lista.sort()

    UltimaFecha = carteira.iloc[-1]['Data da Compra']

    ValoresInvestidos = []

    #=============================================================================
    # CONSTRUIR UM PAINEL INTERATIVO

    dff = DataFrame()

    #=============================================================================




    # Em geral não dá pra somar variáveis de diferentes tipagens, mas nesse caso deu certo
    ColunaFinal = 0


    for nome in lista:

         subcarteira = carteira.loc[ carteira['Ativo'] == nome ]

         subcarteira = subcarteira.reset_index(drop = True, inplace = False)

         subcarteira['Q_k'] = Soma(subcarteira)

         subcarteira['X_k'] = Media(subcarteira)

         df = yahoo(nome,subcarteira)

         df.drop(columns = ['High', 'Low', 'Open', 'Volume', 'Adj Close'],
                 inplace = True)

         df['Q_k'], df['X_k'] = Copias(subcarteira,df)

         df['Variação Total (R$)'] = df['Q_k'] * (df['Close'] - df['X_k'])

         df['Variação Percentual'] = (df['Close'] / df['X_k']) -1

         df['Nome'] = nome
         dff = concat([dff,df])

         #-------------------------------------------------------------------------------------------

         subcarteira['Valor Investido (R$)'] = subcarteira['Quantidade'] * subcarteira['Compra (R$)']

         ValoresInvestidos.append(sum(subcarteira['Valor Investido (R$)']))

         ColunaFinal = ColunaFinal + array(df.loc[UltimaFecha:]['Variação Total (R$)'])


    TotalInvestido = sum(ValoresInvestidos)

    DICIONARIO = {'Variação Total (R$)':ColunaFinal}

    novatabela = DataFrame(data = DICIONARIO,
                           index = df.loc[UltimaFecha:].index)

    novatabela['Variação Percentual'] = novatabela['Variação Total (R$)']/TotalInvestido

    novatabela['Nome'] = 'Carteira'


    dff.drop(columns = ['Close', 'Q_k', 'X_k'], inplace = True)
    dff = concat([dff,novatabela])

    dff.reset_index(inplace = True)

    dff['Variação Total (R$)'] = dff['Variação Total (R$)'].apply(lambda x : round(x,2))
    dff['Variação Percentual'] = dff['Variação Percentual'].apply(lambda x : round(x,4))

    return dff


if __name__ == '__main__':
    from entrada import leitura

    # INSERIR A CARETEIRA TESTE
    teste = leitura('CarteiraTeste.csv')

    historicos = GeracaoTabela(teste)

    print(historicos.sample(10))
