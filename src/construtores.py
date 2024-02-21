import os
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt


def gerar_df(arquivo_txt, dados_orientacao=None):
    arquivo = open(arquivo_txt)
    linhas = arquivo.readlines()

    dados = []

    '''1 - Retirando o Cabeçalho, transformando string em float e montando o dataframe'''
    for linha in linhas[16:]:
        virgula = linha.find(",")
        virgula_2 = linha[virgula + 1:].find(",") + virgula + 1
        virgula_3 = linha[virgula_2 + 1:].find(",") + virgula_2 + 1

        timestamp = linha[:virgula]
        eixo_x = linha[virgula + 1:virgula_2]
        eixo_y = linha[virgula_2 + 1:virgula_3]
        eixo_z = linha[virgula_3 + 1:]

        linha_dados = [float(timestamp), float(eixo_x), float(eixo_y), float(eixo_z)]
        dados.append(linha_dados)
    if dados_orientacao == "sim":
        df = pd.DataFrame(dados, columns=["Timestamp", "Azimuth", "Pitch", "Roll"])
    else:
        df = pd.DataFrame(dados, columns=["Timestamp", "Eixo X", "Eixo Y", "Eixo Z"])

    tempo_segundos = [0.000]
    i = 0

    while i < len(df["Timestamp"]):
        if i != len(df["Timestamp"]) - 1:
            variacao_tempo = (df["Timestamp"][i + 1]) - (df["Timestamp"][0])
            temp_seg = variacao_tempo / 1000000000
            tempo_segundos.append(temp_seg)

        i += 1

    df.insert(1, "Tempo [s]", tempo_segundos, True)

    return df


def gerar_df_mag(df):
    '''2 - Criando as colunas de força resultante e Tempo [s] '''
    forca_resultante = []
    i = 0

    while i < len(df["Eixo X"]):
        resultante = math.sqrt((df["Eixo X"][i]) ** 2 + (df["Eixo Y"][i]) ** 2 + (df["Eixo Z"][i]) ** 2)
        forca_resultante.append(resultante)
        i += 1

    df["Magnitude [g]"] = forca_resultante

    return df


def gerar_grafico(array, diretorio, numero_imagem, acao=None):
    plt.figure(figsize=(5.16, 3))
    if acao == "transformada":
        plt.ylim(0, 200)
    else:
        plt.ylim(0, 3.2)
    plt.axis('off')
    plt.plot((array), color='gray')
    nome_figura = numero_imagem
    plt.savefig(os.path.join(diretorio, nome_figura))


def transformada(serie_temporal):
    serie_temp_alterada = []
    media_serie_temp = np.mean(serie_temporal)

    for i in serie_temporal:
        dado = i - media_serie_temp
        serie_temp_alterada.append(dado)
    serie_temp_alt = np.array(serie_temp_alterada)

    return np.abs(np.fft.fft(serie_temp_alt))


def criar_array_queda(rotulos, lista_array_de_dados,df, diretorio, chave,gerar_imagem=None,sensor=None, tipo_de_dominio=None):
    sumario = {0: 'Magnitude [g]', 1: 'Eixo X', 2: 'Eixo Y', 3: 'Eixo Z',
               4: 'Azimuth', 5: 'Pitch', 6: 'Roll'}

    if sensor == "GYR":
        tamanho_do_array = 1000
    else:
        tamanho_do_array = 400

    feature = sumario.get(chave)
    coluna_de_dados = df[feature].iloc[0:tamanho_do_array]
    array_dados = np.array(coluna_de_dados)

    if tipo_de_dominio == "freq":
        array_transformada = transformada(array_dados)
        array_dados_tra = array_transformada[:tamanho_do_array / 2]
        array_dados_exp = np.expand_dims(array_dados_tra, axis=1)
        lista_array_de_dados.append(array_dados_exp)

        if gerar_imagem == "sim":
            numero_imagem = str(len(lista_array_de_dados) - 1)
            gerar_grafico(array_dados_tra, diretorio, numero_imagem, "transformada")
    else:
        array_dados_exp = np.expand_dims(array_dados, axis=1)
        lista_array_de_dados.append(array_dados_exp)

        if gerar_imagem == "sim":
            numero_imagem = str(len(lista_array_de_dados) - 1)
            gerar_grafico(array_dados, diretorio, numero_imagem)

    rotulos.append(0)


def criar_array_adl(rotulos, lista_array_de_dados,df, diretorio, chave,gerar_imagem=None,sensor=None, tipo_de_dominio=None):
    sumario = {0: 'Magnitude [g]', 1: 'Eixo X', 2: 'Eixo Y', 3: 'Eixo Z',
               4: 'Azimuth', 5: 'Pitch', 6: 'Roll'}

    if sensor == "GYR":
        tamanho_do_array = 1000
    else:
        tamanho_do_array = 400

    feature = sumario.get(chave)

    div = math.floor(len(df[feature]) / tamanho_do_array)
    a = 0
    b = tamanho_do_array

    for i in range(div):
        coluna_de_dados = df[feature].iloc[a:b]
        array_dados = np.array(coluna_de_dados)

        if tipo_de_dominio == "freq":

            array_transformada = transformada(array_dados)
            array_dados_tra = array_transformada[:tamanho_do_array / 2]
            array_dados_exp = np.expand_dims(array_dados_tra, axis=1)

            tam = len(array_dados_tra)

            if tam == tamanho_do_array/2:

                lista_array_de_dados.append(array_dados_exp)

                if gerar_imagem == "sim":
                    numero_imagem = str(len(lista_array_de_dados) - 1)
                    gerar_grafico(array_dados_tra, diretorio, numero_imagem, "transformada")

        else:
            array_dados_exp = np.expand_dims(array_dados, axis=1)
            tam = len(array_dados)

            if tam == tamanho_do_array:

                lista_array_de_dados.append(array_dados_exp)

                if gerar_imagem == "sim":
                    numero_imagem = str(len(lista_array_de_dados) - 1)
                    gerar_grafico(array_dados, diretorio, numero_imagem)

    a += tamanho_do_array
    b += tamanho_do_array

    rotulos.append(1)






