# python main.py --ip 0.0.0.0 --port 8000

from models.ipkiss import Ipkiss
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
#from datetime import datetime
import imutils
import time
import cv2

#a saída e uma trava usada para garantir a segurança de threads
# trocas dos quadros na saída
saida = None
trava = threading.Lock()
classificador = open('classificadores/haarcascade_frontalface_default.xml')
app = Flask(__name__)

vs = VideoStream(src=0).start()
time.sleep(2.0)

@app.route("/")
def index():
    # retona a view renderizada
    return render_template("index.html")

def detectar_faces(contador):

    global vs, saida, trava
    fd = Ipkiss(fps=0.1)
    total = 0
    while True:
        frame =  vs.read()
        frame = imutils.resize(frame, width=400)
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if total > contador:

            faces = fd.detectar(cinza)
            for (x, y, largura, altura) in faces:
                cv2.rectangle(frame, (x, y), (x + largura, y + altura), (0, 0, 255), 2)

        fd.atualizar(cinza)
        total += 1
        with trava:
            saida = frame.copy()
def gerar():

    global saida, trava

    while True:

        with trava:
            if saida is None:
                continue
            (flag, imagem_codificada) = cv2.imencode(".jpg", saida)

            if not flag:
                continue

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
            bytearray(imagem_codificada) + b'\r\n')

@app.route("/video_raiz")
def video_raiz():
    return Response(gerar(), mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    # construa the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
        help="ensira a porta de ip")
    ap.add_argument("-o", "--port", type=int, required=True,
        help="ensira a porta (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
        help="#frames para construir o fundo")
    args = vars(ap.parse_args())

    t = threading.Thread(target=detectar_faces, args=(
        args["frame_count"],))
    t.daemon = True
    t.start()

    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

vs.stop()