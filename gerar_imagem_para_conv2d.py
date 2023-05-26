import os
import pandas as pd
import math
import matplotlib.pyplot as plt
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

def plot_transformada(frequencias, transformada,nome):
    plt.figure(figsize=(5.16, 3))
    plt.plot(frequencias, transformada,color='gray')
    plt.ylim(0, 200)
    plt.axis('off')
    plt.savefig(nome)

def plot_mag(tempo,mag,nome):
    plt.figure(figsize=(5.16, 3))
    plt.plot(tempo, mag, color='gray')
    plt.legend()
    plt.ylim(0, 3.2)
    plt.axis('off')
    plt.savefig(nome)

def gerar_grafico_queda(df,tipo):

    nome_figura = f"{arquivo[:12]}"
    tempo = df['Tempo [s]']
    magnitude = df['Magnitude [g]']
    div = int(len(magnitude) / 2)

    mag = magnitude.iloc[:div]
    t = tempo.iloc[:div]
    if tipo == "dominio_tempo":
        plot_mag(t, mag,nome_figura)
    elif tipo == "dominio_frequencia":
        plot_transformada(frequencias(t),transformada(mag),nome_figura)

def gerar_grafico6s(df,tipo):

    nome_figura = f"{arquivo[:12]}"
    tempo = df['Tempo [s]']
    magnitude = df['Magnitude [g]']
    div = int((len(magnitude) / 6)*5)

    mag = magnitude.iloc[:(div)]
    t = tempo.iloc[:div]
    if tipo == "dominio_tempo":
        plot_mag(t, mag, nome_figura)
    elif tipo == "dominio_frequencia":
        plot_transformada(frequencias(t),transformada(mag),nome_figura)

def gerar_grafico_adl(df,x,tipo):

    i=0
    tempo = df['Tempo [s]']
    magnitude = df['Magnitude [g]']
    div = int(len(magnitude) / x)
    a = 0
    b = div

    while i < x:

        nome_figura = f"{arquivo[:12]}_{i}.png"
        mag = magnitude.iloc[a:b]
        t = tempo.iloc[a:b]
        if tipo == "dominio_tempo":
            plot_mag(t, mag, nome_figura)
        elif tipo == "dominio_frequencia":
            plot_transformada(frequencias(t), transformada(mag), nome_figura)

        if i < x-1:
            a += div
            b += div

        i +=1


pasta = "/home/dev/PycharmProjects/FallDetection/conv/dados/saindo do carro"
lista_arquivos = os.listdir(pasta)

for arquivo in lista_arquivos:
    gerar_grafico6s(gerar_df(arquivo),"dominio_frequencia")