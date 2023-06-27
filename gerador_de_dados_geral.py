import os
import pandas as pd
import math
import random
import numpy as np
import matplotlib.pyplot as plt

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

def gerar_grafico(array,diretorio,numero_imagem,acao=None):
    plt.figure(figsize=(5.16,3))
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

def criar_array_queda(df,rotulo,diretorio):
    magnitude = df['Magnitude [g]'].iloc[0:400]

    array_mag = np.array(magnitude)
    array_mag_exp = np.expand_dims(array_mag, axis=1)

    arrays_mag_tempo.append(array_mag_exp)
    rotulos.append(rotulo)
    numero_imagem = str(len(arrays_mag_tempo))
    gerar_grafico(array_mag, diretorio,numero_imagem)

def criar_array_queda_transformada(df,diretorio):
    magnitude = df['Magnitude [g]'].iloc[0:400]

    array_mag = np.array(magnitude)
    array_mag = transformada(array_mag)
    array_mag = array_mag[:200]
    array_mag_exp = np.expand_dims(array_mag, axis=1)

    arrays_mag_freq.append(array_mag_exp)
    numero_imagem = str(len(arrays_mag_freq))
    gerar_grafico(array_mag, diretorio,numero_imagem,"transformada")

def criar_array_adl_transfomada(df,diretorio):
    div = math.floor(len(df['Magnitude [g]']) / 400)
    a = 0
    b = 400

    for i in range(div):
        magnitude = df['Magnitude [g]'].iloc[a:b]
        array_mag = np.array(magnitude)
        array_mag = transformada(array_mag)
        array_fourier = array_mag[:200]
        array_fourier_exp = np.expand_dims(array_fourier, axis=1)

        tam = len(array_mag)

        if tam == 400:

            arrays_mag_freq.append(array_fourier_exp)
            numero_imagem = str(len(arrays_mag_freq))
            gerar_grafico(array_fourier, diretorio, numero_imagem, "transformada")

            a += 400
            b += 400

def criar_array_adl(df,rotulo,diretorio):
        div = math.floor(len(df['Magnitude [g]'])/400)
        a = 0
        b = 400

        for i in range(div):
            magnitude = df['Magnitude [g]'].iloc[a:b]
            array_mag = np.array(magnitude)
            array_mag_exp= np.expand_dims(array_mag, axis=1)
            tam = len(array_mag)

            if tam == 400:
                    rotulos.append(rotulo)
                    arrays_mag_tempo.append(array_mag_exp)
                    numero_imagem = str(len(arrays_mag_tempo))
                    gerar_grafico(array_mag, diretorio, numero_imagem)

            a += 400
            b += 400

pasta = "/home/dev/PycharmProjects/FallDetection/conv/dados/todos"

diretorio = "/home/dev/PycharmProjects/FallDetection/conv/Novo cj de dados/Conv2d/Dominio do Tempo/Todas as Imagens"
diretorio2 = "/home/dev/PycharmProjects/FallDetection/conv/Novo cj de dados/Conv2d/Dominio da Frequencia/Todas as Imagens"
diretorio3 = "/home/dev/PycharmProjects/FallDetection/conv/Novo cj de dados/Conv1d/Dominio da Frequencia/Todos os arrays"
diretorio4 = "/home/dev/PycharmProjects/FallDetection/conv/Novo cj de dados/Conv1d/Dominio do Tempo/todos os arrays"
diretorio5 = "/home/dev/PycharmProjects/FallDetection/conv/Novo cj de dados"

lista_arquivos = os.listdir(pasta)
arrays_mag_tempo = []
arrays_mag_freq = []
rotulos = []

for arquivo in lista_arquivos:
    caminho_arquivo = os.path.join(pasta, arquivo)

    if os.path.exists(caminho_arquivo):
        if arquivo in os.listdir('/home/dev/PycharmProjects/FallDetection/conv/dados/queda'):
            criar_array_queda(gerar_df(arquivo),0,diretorio)
            criar_array_queda_transformada(gerar_df(arquivo),diretorio2)

        else:
            criar_array_adl(gerar_df(arquivo),1,diretorio)
            criar_array_adl_transfomada(gerar_df(arquivo),diretorio2)

arrays_mag_tempo = np.asarray(arrays_mag_tempo)
arrays_mag_freq = np.asarray(arrays_mag_freq)
rotulos_array = np.asarray(rotulos)

np.save(os.path.join(diretorio4, 'dados_tempo.npy'), arrays_mag_tempo)
np.save(os.path.join(diretorio3, 'dados_freq.npy'), arrays_mag_freq)

np.save(os.path.join(diretorio5, 'rotulos.npy'), rotulos_array)

