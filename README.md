# Analise_Impress-o_Digital
Codigo de Análise de tipo de Impressão Digital baseado no sistema Henry
Este codigo foi feito com base no codigo de reconhecimento facial do sitio:
https://www.pytorials.com/face-recognition-using-opencv-part-3/


Trata-se de um rede neural convolutiva desenvolvida para reconhecimento facial que foi modificada para reconhecer os tipos de impressão digital baseando-se no sistema Henry:

1- Arco - as linhas dactilares formam-se de um lado e tendem a sair do outro lado da digital. Mostram forma abaulada e não apresentam deltas ou com uma elevação acentuada no centro da imagem no formato de uma tenda.

2- Presilha - as linhas dactilares curvam-se no centro e tendem a retornar para o mesmo lado de formação e apresentam uma formação nuclear no lado oposto ao loda de formação das linhas curvas.

3- Verticilo - apresenta dois deltas: um a direita e outro a esquerda do núcleo. As cristas internas a esses deltas apresentam um padrão concêntrico, espiralado, oval ou mesmo sinuoso com um centro bem definido.

4- Não reconhecido pelo sistema - ou seja, por motivos de qualidade, baixo contraste, excesso de pressão no sensor, ruido ou que por outros motivos, não permitiu o reconhecimento do padrão.

