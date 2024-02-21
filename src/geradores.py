import os
import construtores
import numpy as np

def popular_lista_arquivos(sensor, subdiretorio_quedas):

    lista_arquivos = []
    for subdiretorio_nivel_1 in os.listdir(subdiretorio_quedas):
        subdiretorio_path_nivel_1 = os.path.join(subdiretorio_quedas, subdiretorio_nivel_1)

        if os.path.isdir(subdiretorio_path_nivel_1):
            subdiretorio_nivel_2 = set(os.listdir(subdiretorio_path_nivel_1))
            acc_path = os.path.join(subdiretorio_path_nivel_1,sensor)
            lista_arquivos_dir = os.listdir(acc_path)
            for arquivo in lista_arquivos_dir:
                caminho_arquivo = os.path.join(acc_path, arquivo)
                lista_arquivos.append(caminho_arquivo)

    return lista_arquivos

def gerador_de_arquivos(subdiretorio_quedas,diretorio_dados, diretorio_imagens_tempo,diretorio_imagnes_freq, chave, gerar_imagem, sensor, nome, dados_orientacao):

    lista_arquivos =  popular_lista_arquivos(sensor,subdiretorio_quedas)

    arrays_time_domain = []
    arrays_freq_domain = []
    rotulos = []

    for arquivo in lista_arquivos:
        if os.path.exists(arquivo):
            if chave == 0:
                df = construtores.gerar_df_mag(construtores.gerar_df(arquivo))
            else:
                df = construtores.gerar_df(arquivo,dados_orientacao)

            if "BSC" in arquivo or "FOL" in arquivo or "SDL" in arquivo or "FKL" in arquivo:

                construtores.criar_array_queda(rotulos, arrays_time_domain, df, diretorio_imagens_tempo, chave, gerar_imagem, sensor)
                construtores.criar_array_queda(rotulos, arrays_freq_domain,df, diretorio_imagnes_freq, chave, gerar_imagem, sensor, 'freq')
        else:
            construtores.criar_array_adl(rotulos, arrays_time_domain, df, diretorio_imagens_tempo, chave, gerar_imagem, sensor)
            construtores.criar_array_adl(rotulos, arrays_freq_domain,df, diretorio_imagnes_freq, chave, gerar_imagem, sensor, 'freq')

    arrays_tempo = np.asarray(arrays_time_domain)
    arrays_freq = np.asarray(arrays_freq_domain)
    rotulos_array = np.asarray(rotulos)

    np.save(os.path.join(diretorio_dados, f'{sensor}_{nome}_tempo.npy'), arrays_tempo)
    np.save(os.path.join(diretorio_dados, f'{sensor}_{nome}_freq.npy'), arrays_freq)
    np.save(os.path.join(diretorio_dados, f'{sensor}_{nome}_rotulos.npy'), rotulos_array)
