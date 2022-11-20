from pandas import read_csv, DataFrame
from datetime import datetime


def leitura(arquivo):
    carteira = read_csv(arquivo,
                        sep = ';',
                        decimal = ',',
                        parse_dates = ['Data da Compra'],
                        date_parser = lambda fecha : datetime.strptime(fecha, '%d/%m/%Y'))

    return carteira

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


if __name__ == '__main__':

    inicio = leitura('CarteiraTeste.csv')

    print(inicio.sample(5))
