import pandas as pd
import os
import math
import matplotlib.pyplot as plt



def ordenar_por_numero(id):
    return int(id[2:])

def adicionar_coluna_de_magnitude(dataframe,sensor = None):
    letra_inicial = None

    if sensor == "acc":
        letra_inicial = "a"
    else:
        letra_inicial = "w"

    forca_resultante = []
    i = 0

    while i < len(dataframe[f'{letra_inicial}x']):
        resultante = math.sqrt((dataframe[f'{letra_inicial}x'][i]) ** 2 + (dataframe[f'{letra_inicial}y'][i]) ** 2 + (dataframe[f'{letra_inicial}z'][i]) ** 2)
        forca_resultante.append(resultante)
        i += 1
    dataframe.insert(5, "Magnitude", forca_resultante, True)

def gerar_serie_de_tempo(timestamp):
    timestamp = timestamp.reset_index(drop=True)
    timestamp = timestamp.drop(0)
    timestamp = timestamp.reset_index(drop=True)

    tempo_segundos = [0.000]
    k = 0
    while k < len(timestamp):
        if k!= len(timestamp) - 1:
            variacao_tempo = (timestamp[k + 1]) - (timestamp[0])
            temp_seg = variacao_tempo / 1000
            tempo_segundos.append(temp_seg)

        k += 1
    return tempo_segundos

def plot_grafico(array,tempo,nome_figura,diretorio,arquivo_erros):
    try:
        plt.ylim(-80, 150)
        plt.plot(tempo,array,label="Magnitude")
        plt.legend()
        plt.xlabel("Time")
        plt.savefig(os.path.join(diretorio,nome_figura))
        plt.close()
    except Exception as e:
        mensagem_erro = f"Erro ao plotar o gráfico {nome_figura}: {str(e)}"
        print(mensagem_erro)

        # Registrar o erro em um arquivo
        with open(arquivo_erros, "a") as arquivo:
            arquivo.write(mensagem_erro + "\n")

def obter_caminhos_dos_arquivos(diretorio_principal, subdiretorio, posicao):
    caminho_do_subdiretorio = os.path.join(diretorio_principal, subdiretorio)
    caminho_do_subdiretorio_do_subdiretorio = os.path.join(caminho_do_subdiretorio, posicao)

    nome_do_arquivo = f'{subdiretorio}_{posicao}_acceleration.csv'
    nome_do_arquivo_2 = f'{subdiretorio}_{posicao}_sampling.csv'
    nome_do_arquivo_3 = f'{subdiretorio}_{posicao}_angular_speed.csv'

    arquivo_sampling = os.path.join(caminho_do_subdiretorio_do_subdiretorio, nome_do_arquivo_2)
    arquivo_acc = os.path.join(caminho_do_subdiretorio_do_subdiretorio, nome_do_arquivo)
    arquivo_gir = os.path.join(caminho_do_subdiretorio_do_subdiretorio, nome_do_arquivo_3)

    return arquivo_acc,arquivo_gir,arquivo_sampling

def gerar_dataframe(arquivo_acc,arquivo_gir,arquivo_sampling):

    acc = pd.DataFrame(pd.read_csv(arquivo_acc))
    gir = pd.DataFrame(pd.read_csv(arquivo_gir))
    sampling = pd.DataFrame(pd.read_csv(arquivo_sampling))

    adicionar_coluna_de_magnitude(acc,"acc")
    adicionar_coluna_de_magnitude(gir)

    return acc,gir,sampling

def seccionar_array_de_dados(df_acc,df_gir,i):
    magacc = df_acc.loc[df_acc["sampling"] == i, "Magnitude"]
    magacc = magacc.reset_index(drop=True)
    magacc = magacc.drop(0)

    xacc = df_acc.loc[df_acc["sampling"] == i, "ax"]
    xacc = xacc.reset_index(drop=True)
    xacc = xacc.drop(0)

    yacc = df_acc.loc[df_acc["sampling"] == i, "ay"]
    yacc = yacc.reset_index(drop=True)
    yacc = yacc.drop(0)

    zacc = df_acc.loc[df_acc["sampling"] == i, "az"]
    zacc = zacc.reset_index(drop=True)
    zacc = zacc.drop(0)

    maggir = df_gir.loc[df_gir["sampling"] == i, "Magnitude"]
    maggir = maggir.reset_index(drop=True)
    maggir = maggir.drop(0)

    xgir = df_gir.loc[df_gir["sampling"] == i, "wx"]
    xgir = xgir.reset_index(drop=True)
    xgir = xgir.drop(0)

    ygir = df_gir.loc[df_gir["sampling"] == i, "wy"]
    ygir = ygir.reset_index(drop=True)
    ygir = ygir.drop(0)

    zgir = df_gir.loc[df_gir["sampling"] == i, "wz"]
    zgir = zgir.reset_index(drop=True)
    zgir = zgir.drop(0)

    timestamp_acc = df_acc.loc[df_acc["sampling"] == i, "timestamp"]
    timestamp_gir = df_gir.loc[df_gir["sampling"] == i, "timestamp"]
    tempo_segundos_acc = gerar_serie_de_tempo(timestamp_acc)
    tempo_segundos_gir = gerar_serie_de_tempo(timestamp_gir)

    return magacc,xacc,yacc,zacc,tempo_segundos_acc,maggir,xgir,ygir,zgir,tempo_segundos_gir

def plotar_grafico_das_atividade(i,lista_de_nomes,df_sampling,magacc,xacc,yacc,zacc,tempo_segundos_acc,maggir,xgir,ygir,zgir,tempo_segundos_gir,
                                 diretorio1, diretorio2, diretorio3, diretorio4, diretorio5,diretorio6,diretorio7,diretorio8,arquivo_erros):
    atividade = (df_sampling.loc[df_sampling["id"] == i, "exercise"].iloc[0])

    if (df_sampling.loc[df_sampling["id"] == i, "withRifle"].iloc[0]) == 1:
        atividade = f'{atividade}_with_rifle'

    nome_figura = f'ID{(df_sampling.loc[df_sampling["id"] == i, "userId"].iloc[0])}_{atividade}'

    lista_de_nomes.append(nome_figura)
    cont = 0
    for j in range(len(lista_de_nomes)):
        if lista_de_nomes[j] == nome_figura:
            cont += 1

    nome_figura_definitivo = f'{nome_figura}.{cont}.png'

    plot_grafico(magacc, tempo_segundos_acc, nome_figura_definitivo, diretorio1, arquivo_erros)
    plot_grafico(xacc, tempo_segundos_acc, nome_figura_definitivo, diretorio2, arquivo_erros)
    plot_grafico(yacc, tempo_segundos_acc, nome_figura_definitivo, diretorio3, arquivo_erros)
    plot_grafico(zacc, tempo_segundos_acc, nome_figura_definitivo, diretorio4, arquivo_erros)

    plot_grafico(maggir, tempo_segundos_gir, nome_figura_definitivo, diretorio5, arquivo_erros)
    plot_grafico(xgir, tempo_segundos_gir, nome_figura_definitivo, diretorio6, arquivo_erros)
    plot_grafico(ygir, tempo_segundos_gir, nome_figura_definitivo, diretorio7, arquivo_erros)
    plot_grafico(zgir, tempo_segundos_gir, nome_figura_definitivo, diretorio8, arquivo_erros)

def criar_array_queda( magacc,xacc,yacc,zacc,tempo_segundos_acc,maggir,xgir,ygir,zgir,tempo_segundos_gir ):

    labels_multiplos = {"ADL_1": 0,"ADL_2": 1,"ADL_3": 2,"ADL_4": 3,"ADL_5": 4,"ADL_6": 5,"ADL_7": 6,"ADL_8": 7,"ADL_11": 8,"ADL_12": 9,"ADL_13": 10,"ADL_14": 11,"ADL_15": 12,"OM_1": 13,"OM_2": 14,
              "OM_3": 15,"OM_4": 16,"OM_5": 17,"OM_6": 18,"OM_7": 19,"OM_8": 20,"OM_9": 21,"FALL_1": 22,"FALL_2": 23,"FALL_3": 24,"FALL_5": 25,"FALL_6": 25}

    labels_tres = {"ADL_1": 1, "ADL_2": 1, "ADL_3": 1, "ADL_4": 1, "ADL_5": 1, "ADL_6": 1, "ADL_7": 1, "ADL_8": 1,
                       "ADL_11": 1, "ADL_12": 1, "ADL_13": 1, "ADL_14": 1, "ADL_15": 1, "OM_1": 2,
                       "OM_2": 2, "OM_3": 2, "OM_4": 2, "OM_5": 2, "OM_6": 2, "OM_7": 2, "OM_8": 2, "OM_9": 2,
                       "FALL_1": 0, "FALL_2": 0, "FALL_3": 0, "FALL_5": 0, "FALL_6": 0}


    '''Labels binario 1 as atividades 0M6 a OM8 são consideradas como quedas'''
    labels_binario1 = {"ADL_1": 1, "ADL_2": 1, "ADL_3": 1, "ADL_4": 1, "ADL_5": 1, "ADL_6": 1, "ADL_7": 1, "ADL_8": 1,"ADL_11": 1, "ADL_12": 1, "ADL_13": 1, "ADL_14": 1, "ADL_15": 1,"OM_1": 1,
                      "OM_2": 1,"OM_3": 1, "OM_4": 1, "OM_5": 1, "OM_6":0 , "OM_7":0 , "OM_8":0 , "OM_9": 1,"FALL_1": 0, "FALL_2": 0, "FALL_3": 0, "FALL_5": 0, "FALL_6": 0}

    '''Labels binario 2 as atividades 0M6 a OM8 são consideradas como não quedas'''
    labels_binario2 = {"ADL_1": 1, "ADL_2": 1, "ADL_3": 1, "ADL_4": 1, "ADL_5": 1, "ADL_6": 1, "ADL_7": 1, "ADL_8": 1,"ADL_11": 1, "ADL_12": 1, "ADL_13": 1, "ADL_14": 1, "ADL_15": 1, "OM_1": 1,
                       "OM_2": 1, "OM_3": 1, "OM_4": 1, "OM_5": 1, "OM_6": 0, "OM_7": 0, "OM_8": 0, "OM_9": 1,"FALL_1": 0, "FALL_2": 0, "FALL_3": 0, "FALL_5": 0, "FALL_6": 0}





def plotar_atividades(df_acc,df_gir,df_sampling,diretorio1,diretorio2,diretorio3,diretorio4,diretorio5, diretorio6, diretorio7,
                                     diretorio8,arquivo_erros):
    lista_de_nomes = []

    for i in (df_sampling["id"]):

        magacc,xacc,yacc,zacc,tempo_segundos_acc,maggir,xgir,ygir,zgir,tempo_segundos_gir = seccionar_array_de_dados(df_acc,df_gir,i)

        plotar_grafico_das_atividade(i, lista_de_nomes,df_sampling, magacc, xacc, yacc, zacc, tempo_segundos_acc, maggir, xgir,ygir, zgir,
                                     tempo_segundos_gir,diretorio1, diretorio2, diretorio3, diretorio4, diretorio5, diretorio6, diretorio7,
                                     diretorio8, arquivo_erros)



diretorio_principal= "/home/dev/Área de trabalho/Combatente/Combatente/Database"

lista_de_subdiretorios = os.listdir(diretorio_principal)

lista_de_subdiretorios.sort(key=ordenar_por_numero)

#diretorios acc
diretorio1 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/acelerometro/mag"
diretorio2 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/acelerometro/x"
diretorio3 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/acelerometro/y"
diretorio4 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/acelerometro/z"
#diretorios gir
diretorio5 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/giroscopio/mag"
diretorio6 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/giroscopio/x"
diretorio7 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/giroscopioy"
diretorio8 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/giroscopio/z"

arquivo_erros = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/erros"

posicao = "CHEST"

for subdiretorio in lista_de_subdiretorios:
    acc,gir,sampling = obter_caminhos_dos_arquivos(diretorio_principal, subdiretorio, posicao)
    df_acc,df_gir,df_sampling = gerar_dataframe(acc,gir,sampling)
    plotar_atividades(df_acc, df_gir, df_sampling,diretorio1,diretorio2,diretorio3,diretorio4,diretorio5, diretorio6, diretorio7,
                                     diretorio8,arquivo_erros)

