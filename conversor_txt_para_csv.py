import pandas as pd
import math

arquivo = open('WAL_acc_9_1.txt')
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

#print(df)
df.to_csv("acc.WAL_9.1.csv")
