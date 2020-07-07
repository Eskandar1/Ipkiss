import numpy as np
import imutils
import cv2

class Ipkiss:

    def __init__(self,fps=0.5):
        self.fps = fps
        self.fundo = None
        self.classificador = cv2.CascadeClassifier("classificadores/haarcascade_frontalface_default.xml")

    def atualizar(self, imagem):
        if self.fundo is None:
            self.fundo = imagem.copy().astype("float")
            return
        cv2.accumulateWeighted(imagem, self.fundo, self.fps)

    def detectar(self,imagem_cinza):
        faces = self.classificador.detectMultiScale(imagem_cinza,1.3,5)
        return faces

