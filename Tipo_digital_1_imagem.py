# importa bibliotecas
import warnings

import cv2
from scipy.ndimage import gaussian_filter
from skimage.color import rgb2gray
from skimage import exposure
from skimage.color import rgb2gray
from skimage import io
from skimage.morphology import skeletonize
from skimage.util import invert
from skimage import filters
from skimage import img_as_ubyte

# Variaveis globais do projeto
endereco_xml = (r'D:\Eric\Documentos\Unesc\Grupos de pesquisa\Interpretacao_digitais')
filtro = 25  # limiar confiança de exclusão da classificação, se a confiança foi maior que filtro, classifica como outros
types = ['', 'Arco', 'Presilha', 'Verticilo', 'Outros']  # tipos de classificação treinada


def acompanha_linha(digital, w, h, t):
    # Pre: funça que recebe uma imagem com seu respectivo tamanho (w,h) e tamanho minimo t para aceitar como reta
    # Pos: retorna o numero de retas encontradas com tamanho maior que t
    lines = 0  # seta variavel de contagem de linhas em 0
    possibilities = [-1, 0, 1]  # define a possibilidade de busca de continuidade de linha
    for tentativa in range(2):  # numero de varreduras a serem feitas na imagem
        for i in range(w):  # percorre o comprimento
            for j in range(h):  # percorre a altura
                if digital[i][j] == 0:  # verifica se encontra um ponto escuro
                    side = 0  # inicializa a variavel de contagem de vizinhos
                    for a in possibilities:  # verifica se ha visinhos na direção vertical
                        for b in possibilities:  # verifica se ha vizinhos na horizontal
                            if (i + a >= 0) and (j + b >= 0) and (i + a < w) and (
                                    j + b < h):  # Exclui a busca nas bordas
                                if digital[i + a][j + b] < 0.5:  # caso encontre ponto escuro (<0.5)
                                    side += 1  # conta um vizinho
                    if side <= 2:  # se ao verificar todas os vizinhos o numeorde vizinhos for menor ou igual a doi
                        # print(i,j)
                        digital, tamanho = apaga_linha(digital, w, h, i, j,
                                                       t)  # apaga aquela linha para evitar a contagem repetida regista o tamanho da linha apagada
                        if tamanho >= t:  # se o tamanho for maior ou igual a t
                            lines += 1  # conta a linha
    return lines  # ao final do processo retorna o numero de linhas


def apaga_linha(digital, w, h, x, y, t):  #
    # pre: recebe um imagem, o tamanho dela(w,h), a coordenada da linha e o tamanho limite
    # pos: retorna a imagem com a sem a linha da coordenada (x,y) caso seja menor que t ou com a linha na cor 0.1 para evitar ser recontada e o seu respectivo tamanho
    coordenadas = []  # seta vetor de acompanhamento da linha
    tamanho_linha = 0  # seta variavel de contagem de tamanho
    achoulinha = 1  # seta variavel de verificação de existencia de continuidade da linha
    possibilities = [-1, 0, 1]  # vetor com as possibilidade de vizinhança
    digital[x][y] = 1  # seta ponto (x,y) como branco, ou seja apagou o primero ponto da linha
    coordenadas.append((x, y))  # regista o ponto apagado no vetor
    while (achoulinha == 1):  # enquanto houver continuidade
        achoulinha = 0  # seta continuidade como inexistente
        for a in possibilities:  # verifica a continuidade na vertical
            for b in possibilities:  # verifica continuidade na horizontal
                if (x + a >= 0) and (y + b >= 0) and (x + a < w) and (y + b < h) and (
                        digital[x + a][y + b] == 0):  # caso encontre e não seja borda
                    achoulinha = 1  # seta continuidade
                    tamanho_linha += 1  # conta tamanho da linha
                    x += a  # seta o novo ponto de x
                    y += b  # seta o novo ponto de y
                    coordenadas.append((x, y))  # regista o ponto(x,y) no vetor
                    digital[x][
                        y] = 0.1  # seta o valor do ponto em 0.1 para continuar escuro, mas saber que ja foi contado
    if tamanho_linha < t:  # se o tamanho da linha for menor que t
        for cord in coordenadas:  # precorre o vetor com as coordenadas armazenadas
            xx, yy = cord  # define xx e yy a partir da tupla de endereçamento
            digital[xx][yy] = 1  # define o ponto como branco (1)
    return digital, tamanho_linha  # retorna a nova imagem com a linha apagada e o tamanho da l1nha


def convertefoto(caminho_imagem):
    # pre: Recebe a imagem e converte para uma imagem esqueletizada e binarizada (0=Preto e 1=Branco)
    # Pos: Retorna imagem binarizada e esqueletizada (todas as linha tem 1 pixel de largura)
    with warnings.catch_warnings(): # supressão de avisos de perda de resolução na conversão de tipo de imagem
        warnings.simplefilter("ignore") # comando para ignorar avisos do tipo "ignore"
        image = io.imread(caminho_imagem)  # le a imagem
        grayfoto = rgb2gray(image) # transforma para tons de cinza
        original_shape = image.shape # busca caracteristicas da imagem
        width = original_shape[0] # define comprimento
        height = original_shape[1] #Define altura
        adapted = exposure.equalize_adapthist(grayfoto) # ajusta brihlo e contraste para normalizar a foto
        g = gaussian_filter(adapted, 0.2) # aplica filtro gaussiano para ajustar "pontas"
        thresh = (filters.threshold_otsu(g)) # busca ponto de corte para diferencias os tons de cinza
        binary = (g >= thresh).astype(float) # binariza a imagem sendo menor que o thresh preto=0  e maior branco=1
        digital = invert(skeletonize(invert(binary)).astype(float)) # aplica inverte a imagem (para esquelatizar as digitais e não o fundo), aplica filtro de esqueletização e inverte a imagem para ter fundo branco
        lines = acompanha_linha(digital, width, height, 5) # chama a função buscar linha com tamanho 5 e retorna numero de linhas
        #digital = rgb2gray(digital) #Converte a imagem de RGB para cinza
    return lines, digital # retorna numero de linha e a imagem esqueletizada


def identifica_imagem(folder):
    # pre: recebe a localização da imagem
    # pos: retorna o indice de confiança, o tipo de digital reconhecido e o numero de linhas num vetor de 3 elementos
    digital_recognizer = cv2.face.LBPHFaceRecognizer_create()
    linhas, original = convertefoto(folder)
    digital_recognizer.read(endereco_xml + '\imagens_treinadas.xml')
    label, confidence = digital_recognizer.predict(original)
    if confidence > filtro:
        label = 4
    return [confidence, types[label], linhas]


print(identifica_imagem(r'D:\Eric\Documentos\Unesc\Grupos de pesquisa\Interpretacao_digitais\Imagens_Originais\9139.bmp')) # chama a função de identificação de imagens
