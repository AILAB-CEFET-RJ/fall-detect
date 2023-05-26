import os
import random
import shutil

dir_origem = '/home/dev/PycharmProjects/FallDetection/conv/transformada/DataSet/treino/'
dir_destino = '/home/dev/PycharmProjects/FallDetection/conv/transformada/DataSet/validação/'
dir_destino2 = '/home/dev/PycharmProjects/FallDetection/conv/transformada/DataSet/teste/'


def distribuidor(dir_origem,dir_destino,fase):
    i=0

    while i < 8:

        d_origem = f'{dir_origem}{i}'
        d_destino = f'{dir_destino}{i}'
        # Lista com todos os arquivos do diretório de origem
        arquivos = os.listdir(d_origem)
        # Número de arquivos a serem selecionados aleatoriamente (20%)

        if fase ==1:
            if i == 4 or i == 6:
                n_arquivos = int(len(arquivos) - 200)
            else:
                n_arquivos = int(len(arquivos) * 0.4)
        else:
            n_arquivos = int(len(arquivos) * 0.5)

        # Seleciona aleatoriamente os arquivos
        arquivos_selecionados = random.sample(arquivos, n_arquivos)
        # Move os arquivos selecionados para o diretório de destino
        for arquivo in arquivos_selecionados:
            caminho_arquivo_origem = os.path.join(d_origem, arquivo)
            caminho_arquivo_destino = os.path.join(d_destino, arquivo)
            shutil.move(caminho_arquivo_origem, caminho_arquivo_destino)
        i+=1


distribuidor(dir_origem,dir_destino,1)

distribuidor(dir_destino,dir_destino2,2)
