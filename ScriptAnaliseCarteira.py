#---------------------------------------------------------
# Importação das bibliotecas

from pandas import DataFrame, read_csv, concat
from datetime import datetime, date
from pandas_datareader import data as web
from numpy import average, zeros, array
from matplotlib.pyplot import subplots,show, title

from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


#-----------------------------------------------------------
# Contantes

hoje = date.today()


#---------------------------------------------------------
# Dados de entrada

def LeituraDaCarteira():

    char = input('Você possui uma carteira em .csv pronta? [s/n] ')

    if char == 's':
        arquivo = input('Digite o nome do arquivo incluindo o .csv: ')

        separador = input('Digite o caractere que separa as colunas: ')

        dec = input('Digite o caractere de decimal: ')

        carteira = read_csv(arquivo,
                            sep = separador,
                            decimal = dec,
                            parse_dates = ['Data da Compra'],
                            date_parser = lambda fecha : datetime.strptime(fecha, '%d/%m/%Y'))
    else:
        Ativos = []
        Quantidades = []
        Precos = []
        Fechas = []

        lampada = True
        while lampada:
            Ativos.append(input('\nDigite o código do ativo: '))

            Quantidades.append(int(input('Digite a quantidade comprada: ')))

            Precos.append(float(input('Digite o preço de compra da unidade: ')))

            Fechas.append(input('Digite a data da compra no formato dd/mm/aaaa: '))

            char = input('\nGostaria de inserir mais uma compra na carteira? [s/n]: ')

            if char == 'n':
                lampada = False

                dicionario = {'Ativo':Ativos,
                              'Quantidade':Quantidades,
                              'Compra (R$)':Precos,
                              'Data da Compra':Fechas}

                carteira = DataFrame(dicionario,
                                     parse_dates = ['Data da Compra'],
                                     date_parser = lambda fecha : datetime.strptime(fecha, '%d/%m/%Y'))
    return carteira


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

#--------------------------------------------------------------------------------
# Função que realiza os gráficos das variações
def graficos(df, nome):

    fig, ax1 = subplots()

    ax1.set_xlabel('t')

    ax1.set_ylabel('Variação Total (R$)')
    ax1.plot(df['Variação Total (R$)'], color = 'navy', label = '$\Delta(t)$')
    ax1.legend(loc = 'lower left')
    ax1.grid(axis = 'both', linestyle = '--')

    ax2 = ax1.twinx()

    ax2.set_ylabel('Variação Percentual')
    ax2.plot(df['Variação Percentual'], color = 'green', label = '$\delta(t)$')
    ax2.legend(loc = 'lower right')

    fig.tight_layout()
    title(nome)
    show()




#-------------------------------------------------------
# Arquivos de entrada

carteira = LeituraDaCarteira()

#-----------------------------------------------------------------------------------
# Processamento de dados

carteira.sort_values(by = 'Data da Compra',
                     inplace = True)

lista = list( set(carteira['Ativo']) )

lista.sort()

UltimaFecha = carteira.iloc[-1]['Data da Compra']

ValoresInvestidos = []

#=============================================================================
# TESTE PRA FUTURAMENTE CONSTRUIR UM PAINEL INTERATIVO

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

     #graficos(df,nome)
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

#graficos(novatabela,'Carteira Teste')

dff.drop(columns = ['Close', 'Q_k', 'X_k'], inplace = True)
dff = concat([dff,novatabela])
#dff.reset_index(inplace = True)
dff.to_csv('tabelafinal.csv')#, index = False)
