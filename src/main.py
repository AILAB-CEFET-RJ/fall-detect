import os
import geradores

def criar_diretorio_se_nao_existir(diretorio):
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

subdiretorio_quedas = "../data/mobiActDataSet"

diretorio_imagensAcc_1_tempo ="../data/image/acc/time/mag/time"
diretorio_imagensAcc_1_freq ="../data/image/acc/time/mag/time"
diretorio_imagensAcc_2_tempo ="../data/image/acc/time/Xaxis/time"
diretorio_imagensAcc_2_freq ="../data/image/acc/time/Xaxis/frequency"
diretorio_imagensAcc_3_tempo ="../data/image/acc/time/Yaxis/time"
diretorio_imagensAcc_3_freq ="../data/image/acc/time/Yaxis/frequency"
diretorio_imagensAcc_4_tempo ="../data/image/acc/time/Zaxis/time"
diretorio_imagensAcc_4_freq ="../data/image/acc/time/Zaxis/frequency"

diretorio_imagensGyr_1_tempo ="../data/image/gyr/time/mag/time"
diretorio_imagensGyr_1_freq ="../data/image/gyr/time/mag/time"
diretorio_imagensGyr_2_tempo ="../data/image/gyr/time/Xaxis/time"
diretorio_imagensGyr_2_freq ="../data/image/gyr/time/Xaxis/frequency"
diretorio_imagensGyr_3_tempo ="../data/image/gyr/time/Yaxis/time"
diretorio_imagensGyr_3_freq ="../data/image/gyr/time/Yaxis/frequency"
diretorio_imagensGyr_4_tempo ="../data/image/gyr/time/Zaxis/time"
diretorio_imagensGyr_4_freq ="../data/image/gyr/time/Zaxis/frequency"

diretorio_imagensOri_2_tempo ="../data/image/ori/time/Azimuth/time"
diretorio_imagensOri_2_freq ="../data/image/ori/time/Azimuth/frequency"
diretorio_imagensOri_3_tempo ="../data/image/ori/time/Pitch/time"
diretorio_imagensOri_3_freq ="../data/image/ori/time/Pitch/frequency"
diretorio_imagensOri_4_tempo ="../data/image/ori/time/Roll/time"
diretorio_imagensOri_4_freq ="../data/image/ori/time/Roll/frequency"

diretorio_destino_arrays_de_dados ="../data/labelsAndArrayData"

criar_diretorio_se_nao_existir(subdiretorio_quedas)
criar_diretorio_se_nao_existir(diretorio_imagensAcc_1_tempo)
criar_diretorio_se_nao_existir(diretorio_imagensAcc_1_freq)
criar_diretorio_se_nao_existir(diretorio_imagensAcc_2_tempo)
criar_diretorio_se_nao_existir(diretorio_imagensAcc_2_freq)
criar_diretorio_se_nao_existir(diretorio_imagensAcc_3_tempo)
criar_diretorio_se_nao_existir(diretorio_imagensAcc_3_freq)
criar_diretorio_se_nao_existir(diretorio_imagensAcc_4_tempo)
criar_diretorio_se_nao_existir(diretorio_imagensAcc_4_freq)
criar_diretorio_se_nao_existir(diretorio_imagensGyr_1_tempo)
criar_diretorio_se_nao_existir(diretorio_imagensGyr_1_freq)
criar_diretorio_se_nao_existir(diretorio_imagensGyr_2_tempo)
criar_diretorio_se_nao_existir(diretorio_imagensGyr_2_freq)
criar_diretorio_se_nao_existir(diretorio_imagensGyr_3_tempo)
criar_diretorio_se_nao_existir(diretorio_imagensGyr_3_freq)
criar_diretorio_se_nao_existir(diretorio_imagensGyr_4_tempo)
criar_diretorio_se_nao_existir(diretorio_imagensGyr_4_freq)
criar_diretorio_se_nao_existir(diretorio_imagensOri_2_tempo)
criar_diretorio_se_nao_existir(diretorio_imagensOri_2_freq)
criar_diretorio_se_nao_existir(diretorio_imagensOri_3_tempo)
criar_diretorio_se_nao_existir(diretorio_imagensOri_3_freq)
criar_diretorio_se_nao_existir(diretorio_imagensOri_4_tempo)
criar_diretorio_se_nao_existir(diretorio_imagensOri_4_freq)
criar_diretorio_se_nao_existir(diretorio_destino_arrays_de_dados)

print("Responda com sim ou não")
gerar_imagem = input("Deseja gerar as imagens para a rede convolucional 2D?")


'''Gerar dados para o sensor de Acelerometro:'''

sensor = "ACC"

# Magnitude
geradores.gerador_de_arquivos(subdiretorio_quedas,diretorio_destino_arrays_de_dados,diretorio_imagensAcc_1_tempo,
                              diretorio_imagensAcc_1_freq,0,gerar_imagem,sensor,"mag","não")
#Eixo X
geradores.gerador_de_arquivos(subdiretorio_quedas,diretorio_destino_arrays_de_dados,diretorio_imagensAcc_2_tempo,
                              diretorio_imagensAcc_2_freq,1,gerar_imagem,sensor,"eixoX","não")
#Eixo Y
geradores.gerador_de_arquivos(subdiretorio_quedas,diretorio_destino_arrays_de_dados,diretorio_imagensAcc_3_tempo,
                              diretorio_imagensAcc_3_freq,2,gerar_imagem,sensor,"eixoY","não")
#Eixo Z
geradores.gerador_de_arquivos(subdiretorio_quedas,diretorio_destino_arrays_de_dados,diretorio_imagensAcc_4_tempo,
                              diretorio_imagensAcc_4_freq,3,gerar_imagem,sensor,"eixoZ","não")

'''Gerar dados para o sensor de Giróscopio:'''

sensor = "GYR"

# Magnitude
geradores.gerador_de_arquivos(subdiretorio_quedas,diretorio_destino_arrays_de_dados,diretorio_imagensGyr_1_tempo,
                              diretorio_imagensGyr_1_freq,0,gerar_imagem,sensor,"mag","não")
#Eixo X
geradores.gerador_de_arquivos(subdiretorio_quedas,diretorio_destino_arrays_de_dados,diretorio_imagensGyr_2_tempo,
                              diretorio_imagensGyr_2_freq,1,gerar_imagem,sensor,"eixoX","não")
#Eixo Y
geradores.gerador_de_arquivos(subdiretorio_quedas,diretorio_destino_arrays_de_dados,diretorio_imagensGyr_3_tempo,
                              diretorio_imagensGyr_3_freq,2,gerar_imagem,sensor,"eixoY","não")
#Eixo Z
geradores.gerador_de_arquivos(subdiretorio_quedas,diretorio_destino_arrays_de_dados,diretorio_imagensGyr_4_tempo,
                              diretorio_imagensGyr_4_freq,3,gerar_imagem,sensor,"eixoZ","não")

'''Gerar dados para o sensor de Orientação:'''

#Azimuth
geradores.gerador_de_arquivos(subdiretorio_quedas,diretorio_destino_arrays_de_dados,diretorio_imagensOri_2_tempo,
                              diretorio_imagensOri_2_freq,4,gerar_imagem,sensor,"Azimuth","sim")
#Pitch
geradores.gerador_de_arquivos(subdiretorio_quedas,diretorio_destino_arrays_de_dados,diretorio_imagensOri_3_tempo,
                              diretorio_imagensOri_3_freq,5,gerar_imagem,sensor,"Pitch","sim")
#Roll
geradores.gerador_de_arquivos(subdiretorio_quedas,diretorio_destino_arrays_de_dados,diretorio_imagensOri_4_tempo,
                              diretorio_imagensOri_4_freq,6,gerar_imagem,sensor,"Roll","sim")