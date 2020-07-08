#import numpy as np
#import imutils
import cv2

class Ipkiss:

    def __init__(self,fps=0.5):
        self.fps = fps
        self.fundo = None
        #aqui é chamado o classificador
        self.classificador = cv2.CascadeClassifier("classificadores/haarcascade_frontalface_default.xml")

    def atualizar(self, imagem):
        if self.fundo is None:
            self.fundo = imagem.copy().astype("float")
            return
        #cv2 faz a transição da imagem de fundo para a imagem, dependendo do fps para a velocidade da troca
        cv2.accumulateWeighted(imagem, self.fundo, self.fps)

    def detectar(self,imagem_cinza):
        #a função detectMultiScale, recebe a imagem , a escala e os neightboor que serão comparados para formar o rosto
        #ela retorna faces que contém os pontos cartesianos de onde começa e termina a face
        faces = self.classificador.detectMultiScale(imagem_cinza,1.3,5)
        return faces

