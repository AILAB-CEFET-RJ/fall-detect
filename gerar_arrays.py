import os
import pandas as pd
import math
import random
import numpy as np

def gerar_df(arquivo_txt):

  arquivo = open(arquivo_txt)
  linhas = arquivo.readlines()


  dados = []

  '''1 - Retirando o Cabeçalho, transformando string em float e montando o dataframe'''
  for linha in linhas[16:]:
      virgula = linha.find(",")
      virgula_2 = linha[virgula + 1:].find(",") + virgula + 1
      virgula_3 =linha[virgula_2 + 1:].find(",") + virgula_2 + 1

      timestamp = linha[:virgula]
      eixo_x = linha[virgula + 1:virgula_2]
      eixo_y = linha[virgula_2 + 1:virgula_3]
      eixo_z = linha[virgula_3 + 1:]

      linha_dados = [float(timestamp),float(eixo_x),float(eixo_y),float(eixo_z)]
      dados.append(linha_dados)

  df = pd.DataFrame(dados, columns=["Timestamp","Eixo X","Eixo Y","Eixo Z"])

  '''2 - Criando as colunas de força resultante e Tempo [s] '''
  forca_resultante = []
  tempo_segundos = [0.000]
  i=0

  while i < len(df["Eixo X"]):
      resultante = math.sqrt((df["Eixo X"][i])**2 +(df["Eixo Y"][i])**2 +(df["Eixo Z"][i])**2)
      forca_resultante.append(resultante)

      if i != len(df["Eixo X"])-1:
          variacao_tempo = (df["Timestamp"][i+1]) - (df["Timestamp"][0])
          temp_seg = variacao_tempo/1000000000
          tempo_segundos.append(temp_seg)

      i+=1

  df.insert(1,"Tempo [s]",tempo_segundos,True)
  df["Força resultante"] = forca_resultante

  '''2 - Criando a colunas de magnitude'''

  magnitude = []

  i = 0
  while i < len(df["Eixo X"]):
      mag = df["Força resultante"][i]/9.807
      magnitude.append(mag)

      i += 1

  df.insert(6,"Magnitude [g]",magnitude,True)

  return df


def transformada(serie_temporal):
    serie_temp_alterada = []
    media_serie_temp = np.mean(serie_temporal)

    for i in serie_temporal:
        dado = i - media_serie_temp
        serie_temp_alterada.append(dado)
    serie_temp_alt = np.array(serie_temp_alterada)

    return np.abs(np.fft.fft(serie_temp_alt))

def frequencias(tempo):
    freq = []

    i = 0
    for j in tempo:
        dt = j - i
        i = j
        freq.append(dt)

    array_freq = np.array(freq)
    media_freq = np.mean(array_freq)

    return np.fft.fftfreq(len(tempo), media_freq)

def criar_array_queda(df,rotulo):
    magnitude = df['Magnitude [g]'].iloc[0:400]
    array_mag = np.array(magnitude)

    '''Comentar a linha abaixo se o objetivo 
    for gerar dados no dominio do tempo'''
    array_mag = transformada(array_mag)
    '''__________________________________'''

    array_mag = np.expand_dims(array_mag, axis=1)
    tam = len(array_mag)
    if tam == 400:
        arrays_mag.append(array_mag)
        rotulos.append(rotulo)

def criar_array_adl(df,rotulo):

    if rotulo == 2:
        a = 0
        b = 400
        c = df['Magnitude [g]'].tail(1).index[0]

        for i in range(2):
            magnitude = df['Magnitude [g]'].iloc[a:b]
            array_mag = np.array(magnitude)

            '''Comentar a linha abaixo se o objetivo 
            for gerar dados no dominio do tempo'''
            array_mag = transformada(array_mag)
            '''__________________________________'''

            array_mag = np.expand_dims(array_mag, axis=1)
            tam = len(array_mag)
            if tam == 400:
                arrays_mag.append(array_mag)
                rotulos.append(2)

            a = c - 400
            b = c
    elif rotulo == 4 or rotulo == 6:
        div = math.floor(len(df['Magnitude [g]']) / 400)
        a = 0
        b = 400
        parado = []
        andando =[]
        for i in range(div):
            magnitude = df['Magnitude [g]'].iloc[a:b]
            array_mag = np.array(magnitude)

            '''Comentar a linha abaixo se o objetivo 
            for gerar dados no dominio do tempo'''
            array_mag = transformada(array_mag)
            '''__________________________________'''

            array_mag = np.expand_dims(array_mag, axis=1)
            tam = len(array_mag)
            if tam == 400:
                if rotulo == 4:
                    parado.append(array_mag)
                elif rotulo == 6:
                    andando.append(array_mag)

        if rotulo == 4:
            parado_selecionado = random.sample(parado, int(len(parado) * 0.5))

            for i in parado_selecionado:
                arrays_mag.append(i)
                rotulos.append(4)
        else:
            andando_selecionado = random.sample(andando, int(len(andando) * 0.5))

            for i in andando_selecionado:
                arrays_mag.append(i)
                rotulos.append(6)
    else:
        div = math.floor(len(df['Magnitude [g]'])/400)
        a = 0
        b = 400

        for i in range(div):
            magnitude = df['Magnitude [g]'].iloc[a:b]
            array_mag = np.array(magnitude)

            '''Comentar a linha abaixo se o objetivo 
            for gerar dados no dominio do tempo'''
            array_mag = transformada(array_mag)
            '''__________________________________'''

            array_mag = np.expand_dims(array_mag, axis=1)
            tam = len(array_mag)
            if tam == 400:
                arrays_mag.append(array_mag)
                if rotulo == 1:
                    rotulos.append(1)
                elif rotulo == 5:
                    rotulos.append(5)

            a += 400
            b += 400

pasta = "/home/dev/PycharmProjects/FallDetection/conv/dados/todos"
lista_arquivos = os.listdir(pasta)
arrays_mag = []
parado = []
andando = []
rotulos = []

for arquivo in lista_arquivos:
    caminho_arquivo = os.path.join(pasta, arquivo)

    if os.path.exists(caminho_arquivo):
        if arquivo in os.listdir('/home/dev/PycharmProjects/FallDetection/conv/dados/queda'):
            criar_array_queda(gerar_df(arquivo),0)
        elif arquivo in os.listdir('/home/dev/PycharmProjects/FallDetection/conv/dados/Corrida'):
            criar_array_adl(gerar_df(arquivo), 1)
        elif arquivo in os.listdir('/home/dev/PycharmProjects/FallDetection/conv/dados/escada'):
            criar_array_adl(gerar_df(arquivo), 2)
        elif arquivo in os.listdir('/home/dev/PycharmProjects/FallDetection/conv/dados/carro'):
            criar_array_queda(gerar_df(arquivo),3)
        elif arquivo in os.listdir('/home/dev/PycharmProjects/FallDetection/conv/dados/parado'):
            criar_array_adl(gerar_df(arquivo), 4)
        elif arquivo in os.listdir('/home/dev/PycharmProjects/FallDetection/conv/dados/Pulo'):
            criar_array_adl(gerar_df(arquivo), 5)
        elif arquivo in os.listdir('/home/dev/PycharmProjects/FallDetection/conv/dados/andando'):
            criar_array_adl(gerar_df(arquivo), 6)
        elif arquivo in os.listdir('/home/dev/PycharmProjects/FallDetection/conv/dados/sentando na cadeira'):
            criar_array_queda(gerar_df(arquivo),7)


arrays = np.asarray(arrays_mag)
np.save('dadosfreq.npy', arrays)

rotulos_array = np.asarray(rotulos)
np.save('rotulosfreq.npy', rotulos_array)