# importa bibliotecas
import cv2
import os
import numpy as np
from skimage import exposure
from skimage.color import rgb2gray
from skimage import io
from skimage.morphology import skeletonize,disk
from skimage.util import invert
from skimage import img_as_ubyte
from skimage import feature
from skimage import filters
from sklearn import svm
from sklearn.model_selection import train_test_split
import skimage


#consntantes de projetos
vizinhos=10 # numero de pixels vizinhos
fator_escala=1.02 # fator de escala da foto  - neste cado apliando em 2 % a area de captação
resolucaoPadrao=(122,134) # resolução padrão das imagens
enderecopadrao=r'D:\Eric\Documentos\Unesc\Grupos de pesquisa\Interpretacao_digitais'
modelocarregado=False
MAXX=122
MAXY=134
MAX=MAXX*MAXY+10


# digital_recognizer = cv2.face.LBPHFaceRecognizer_create()



def imprimevetor(vetor):
    for i in vetor:
        print(i)
def acompanha_linha(digital,w,h,t):
    lines = 0
    possibilities = [-1, 0, 1]
    for tentativa in range(2):
        for i in range(w):
            print("%.2f%% concluido"%(((tentativa*w)+(i))/(2*w)*100))
            for j in range(h):
                if digital[i][j] == 0:
                    side = 0
                    for a in possibilities:
                        for b in possibilities:
                            if (i+a>=0) and (j+b>=0) and (i+a<w)and (j+b<h):
                                if digital[i + a][j + b] <0.5:
                                    side += 1
                    if side <= 2:
                        #print(i,j)
                        digital, tamanho= apaga_linha(digital, w, h, i, j, t)
                        if tamanho>=t :
                            lines += 1
    return lines

def apaga_linha (digital,w,h,x,y,t):
    coordenadas=[]
    tamanho_linha=0
    achoulinha=1
    possibilities = [-1, 0, 1]
    digital[x][y]=1
    coordenadas.append((x,y))
    while(achoulinha==1):
        achoulinha=0
        for a in possibilities:
            for b in possibilities:
                if (x+a>=0) and (y+b>=0) and (x+a<w)and (y+b<h) and (digital[x+a][y+b]==0):
                    achoulinha=1
                    tamanho_linha+=1
                    x+=a
                    y+=b
                    coordenadas.append((x, y))
                    digital[x][y] = 0.1
    if tamanho_linha<t:
        for cord in coordenadas:
            xx,yy=cord
            digital[xx][yy]=1
    return digital,tamanho_linha

def convertefoto(caminho_imagem):

    original = io.imread(caminho_imagem)
    #original = img_as_ubyte(caminho_imagem)
    original_shape = original.shape
    width = original_shape[0]
    height = original_shape[1]
    grayfoto=rgb2gray(original)
    adapted=exposure.equalize_adapthist(grayfoto)
    g=ndi.gaussian_filter(adapted,0.2)
    thresh = (filters.threshold_otsu(g))
    binary = (g>=thresh).astype(float)
    digital=invert(skeletonize(invert(binary)).astype(float))
    resto=invert(invert(digital))
    lines=acompanha_linha(digital,width,height,5)
    digital = skimage.color.gray2rgb(digital)
    resto = skimage.color.gray2rgb(resto)
    return lines,digital,resto


def escolhepasta():
    print("Defina o tipo de Digital")
    print("1) Arco")
    print("2) Presilha")
    print("3) Verticilo")
    print("4) Outros")
    escolha=0
    while(escolha<1 or escolha>4):
        escolha=int(input("Digite sua escolha:"))
        if (escolha<1 or escolha>4):
            print("opção invalida, digite novamente")
    return escolha
def organizafotos(inicio=0,quantidade=1):
    origem_path=r'D:\Eric\Documentos\Unesc\Grupos de pesquisa\Interpretacao_digitais\imagens_originais'
    destino_path=r'D:\Eric\Documentos\Unesc\Grupos de pesquisa\Interpretacao_digitais'
    dirs = os.listdir(origem_path)
    #imprimevetor(dirs)
    for i in range(inicio,inicio+quantidade):
        original = io.imread(origem_path+'\\'+dirs[i])
        lines,digital,resto,=convertefoto(origem_path+'\\'+dirs[i])
        #figura=[original,digital]
        figura = [digital]
        io.imshow_collection(figura)
        io.show()
        print(i)
        resposta=escolhepasta()
        if resposta==1:
            folder=r'/Imagens_separadas_originais/arco/'
            io.imsave(destino_path+folder+dirs[i],original)
            folder2 = r'/Imagens_separadas_esqueletizadas/arco/'
            io.imsave(destino_path + folder2 + dirs[i], digital)
        elif resposta==2:
            folder = r'/Imagens_separadas_originais/presilha/'
            io.imsave(destino_path + folder + dirs[i],original)
            folder2 = r'/Imagens_separadas_esqueletizadas/presilha/'
            io.imsave(destino_path + folder2 + dirs[i], digital)
        elif resposta==3:
            folder = r'/Imagens_separadas_originais/verticilo/'
            io.imsave(destino_path + folder + dirs[i],original)
            folder2 = r'/Imagens_separadas_esqueletizadas/verticilo/'
            io.imsave(destino_path + folder2 + dirs[i], digital)
        else:
            folder = r'/Imagens_separadas_originais/outros/'
            io.imsave(destino_path + folder + dirs[i], original)
            folder2 = r'/Imagens_separadas_esqueletizadas/outros/'
            io.imsave(destino_path + folder2 + dirs[i], digital)



def criadados(endereco=r'D:\Eric\Documentos\Unesc\Grupos de pesquisa\Interpretacao_digitais\Imagens_separadas_esqueletizadas'):

    dados=[]
    fotos=[]
    tipos=['Arco','verticilo','presilha','outros']
    for tipo in tipos:
        i=0
        origem_path = endereco + "\\" + tipo
        dirs = os.listdir(origem_path)
        #print(dirs)
        #os.system('pause')
        for dir in dirs:
            original = io.imread(origem_path+'\\'+dir)
            original=rgb2gray(original)
            """width = original.shape[0]
            height = original.shape[1]
            if (width != MAXX or height!=MAXY):
                escalax=MAXX/width
                escalay=MAXY/height
                if escalax>escalay:
                    original = rescale(original, escalay, anti_aliasing=False)
                else:
                    original = rescale(original, escalax, anti_aliasing = False)
                width = original.shape[0]
                height = original.shape[1]"""
            #io.imsave("D:\\Eric\\Documentos\\Unesc\\Grupos de pesquisa\\Interpretacao_digitais\\miniaturas\\"+tipo+str(i)+'.bmp',mini)
            i+=1
            fotos.append(original)
            if tipo.upper() == 'ARCO':
                dados.append(1)
            elif tipo.upper()=='PRESILHA':
                dados.append(2)
            elif tipo.upper()=='VERTICILO':
                dados.append(3)
            else:
                dados.append(4)

    return dados,fotos
def stat(matriz, col):
    s=0
    for var in matriz:
        s+=var[2]
    average=s/len(matriz)
    s=0
    for var in matriz:
        s+=((var[2]-average))**2
    desvpad=(s/(len(matriz)-1))**0.5
    return average,desvpad
def treina():
    dados,fotos=criadados()


    x_train, x_test, y_train, y_test = train_test_split(fotos, dados, test_size=0.10, random_state=2)
    #digital_recognizer.train(x_train, np.array(y_train))  # executa o treinamento
    #digital_recognizer.write(r'D:\Eric\Documentos\Unesc\Grupos de pesquisa\Interpretacao_digitais\imagens_treinadas.xml')  # grava treinamento realizado
    digital_recognizer.read(r'D:\Eric\Documentos\Unesc\Grupos de pesquisa\Interpretacao_digitais\imagens_treinadas.xml')  # le o  treinamento realizado
    i = 0
    acerto=0
    confusion=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    resultados = []
    total=0
    for imagem in x_test:
        label, confidence = digital_recognizer.predict(imagem)
        total+=confidence
        resultados.append([label,y_test[i],confidence,0,0])
        confusion[y_test[i]-1][label-1]+=1
        i+=1
    media, desvpad = stat(resultados, 2)
    filtro=media+0.85*desvpad
    i=0
    for results in resultados:
        if results[2] >= filtro:
            results[3]=results[0]
            results[0]  = 4
            results[4]=True
            acerto += 1
        elif (results[0] == y_test[i]  or results[0]  == 4):
            acerto += 1
        i+=1
    erro = (acerto / i * 100)
    print(media+desvpad)
    print("O indice de acerto foi %.2f" % erro)

    print("Matriz confusão (real nas linhas, modelo nas colunas)")
    imprimevetor(confusion)
    escolha=input("Deseja imprimir todas as decisões (1=sim/2=não)")
    if escolha=='1':
        imprimevetor(resultados)

digital_recognizer = cv2.face.LBPHFaceRecognizer_create()
#organizafotos(61+100+64+34+10+40+40+40+50+50,100) # não apagar, comando de classificação manual dos dados
#organizafotos(800,100) # não apagar, comando de classificação manual dos dados
treina ()