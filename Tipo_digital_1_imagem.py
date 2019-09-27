# importa bibliotecas
import cv2
from scipy.ndimage import gaussian_filter
from skimage.color import rgb2gray
from skimage import exposure
from skimage.color import rgb2gray
from skimage import io
from skimage.morphology import skeletonize
from skimage.util import invert
from skimage import filters
import skimage


endereco_xml=(r'D:\Eric\Documentos\Unesc\Grupos de pesquisa\Interpretacao_digitais')
filtro=25
types=['','Arco','Presilha','Verticilo','Outros']
def acompanha_linha(digital,w,h,t):
    lines = 0
    possibilities = [-1, 0, 1]
    for tentativa in range(2):
        for i in range(w):
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

    image = io.imread(caminho_imagem)
    #original = img_as_ubyte(caminho_imagem)
    grayfoto=rgb2gray(image)
    original_shape = image.shape
    width = original_shape[0]
    height = original_shape[1]
    adapted=exposure.equalize_adapthist(grayfoto)
    g=gaussian_filter(adapted,0.2)
    thresh = (filters.threshold_otsu(g))
    binary = (g>=thresh).astype(float)
    digital=invert(skeletonize(invert(binary)).astype(float))
    lines=acompanha_linha(digital,width,height,5)
    digital = rgb2gray(digital)
    return lines,digital


def identifica_imagem(folder):
    digital_recognizer = cv2.face.LBPHFaceRecognizer_create()
    linhas,original = convertefoto(folder)
    digital_recognizer.read(endereco_xml+'\imagens_treinadas.xml')
    label, confidence = digital_recognizer.predict(original)
    if confidence>filtro :
        label=4
    return [confidence,types[label],linhas]

print(identifica_imagem(r'D:\Eric\Documentos\Unesc\Grupos de pesquisa\Interpretacao_digitais\Imagens_Originais\9139.bmp'))


