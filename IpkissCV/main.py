# python main.py --ip 0.0.0.0 --port 8000
from flask_pymongo import PyMongo
from models.ipkiss import Ipkiss
from imutils.video import VideoStream
from flask import Response, render_template, Flask, jsonify
import threading
import argparse
from dao import DAO
import imutils
import time
import cv2


teste = True

saida = None

trava = threading.Lock()
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'cv'
app.config['MONGO_URI'] = "mongodb+srv://admin:123@ipkiss.bcenh.gcp.mongodb.net/cv?retryWrites=true&w=majority"
mongo = PyMongo(app)
dao = DAO(mongo)

carr = []
#Aqui Video Stream
vs = VideoStream(src=0).start()
time.sleep(2.0)

@app.route("/")
def index():
    # retona a view renderizada
    #datahora = datetime.now()
    #fotos.insert_one({'foto': 'teste'})
    return render_template("index.html")

@app.route('/horas')
def horas():
    x, y = dao.grafico_horas()
    return jsonify({'type': x, 'results': y})

@app.route('/dias')
def dias():
    x, y = dao.grafico_dias()
    return jsonify({'type': x, 'results': y})

@app.route('/meses')
def meses():
    x, y = dao.grafico_meses()
    return jsonify({'type': x, 'results': y})

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

def detectar_faces(contador):
    
    #Variaveis Globais
    global vs, saida, trava, teste, carr
    #intanciando
    fd = Ipkiss(fps=0.1)
    total = 0
    while True:
        #frame recebe as imagens captadas
        frame =  vs.read()
        #imutils renderiza para o tamanho para 400x400px
        frame = imutils.resize(frame, width=400)
        #cinza recebe uma cópia em escala de cinza da imagem
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if total > contador:
            #a função detectar retorna as coordenadas do(s) rosto(s)
            faces = fd.detectar(cinza)
            if not faces == ():
                for (x, y, largura, altura) in faces:
                    #corta o rosto da pessoa detectada
                    rosto = frame[y: y+altura, x: x+largura]
                    rosto = cv2.cvtColor(rosto, cv2.COLOR_BGR2RGB)
                    rosto = imutils.resize(rosto, 100, 100)
                    if teste:
                        img64 = dao.insert_fotos(rosto)
                        if len(carr) < 3:
                            carr.append(img64)
                        else:
                            #teste = False
                            carr.pop(0)
                            carr.append(img64)
                    # cv2 utiliza as coordenas para fazer um retangulo, nesse caso vermelho de 2px
                    cv2.rectangle(frame, (x, y), (x + largura, y + altura), (0, 0, 255), 2)
        #detectando ou não, a imagem é atualizada
        fd.atualizar(cinza)
        total += 1
        with trava:
            saida = frame.copy()
        time.sleep(0.5)
def gerar():
    #Variavel global
    global saida, trava

    while True:
        with trava:
            if saida is None:
                continue
             #imencode transforma em um buffer
            (flag, imagem_codificada) = cv2.imencode(".jpg", saida)

            if not flag:
                continue
        #e imagem codificada se transforma em um array de bytes
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
            bytearray(imagem_codificada) + b'\r\n')

@app.route("/video_raiz")
def video_raiz():
    #quando iniciado, video raiz chama a funcão gerar
    return Response(gerar(), mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/carrosel')
def carrosel():
    return jsonify({'fotos': carr})
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

    #usandos os dados passados
    t = threading.Thread(target=detectar_faces, args=(
        args["frame_count"],))
    t.daemon = True
    t.start()

    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

vs.stop()