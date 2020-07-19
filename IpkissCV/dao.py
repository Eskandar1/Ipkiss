from main import mongo
from datetime import datetime
from helpers import dateHelper
import numpy as np
import cv2
import base64

collection = mongo.db.fotos


def insert_fotos(imagem):
    data, hora = str(datetime.now()).split(' ')
    img = cv2.imencode('.jpeg', imagem)[1].tostring()
    img64 = base64.b64encode(img).decode()
    local = 'casa'
    dicionario = {
        'imagem': img64,
        'data': data,
        'hora': hora,
        'local': local
    }
    collection.insert_one(dicionario)


def grafico_horas():
    results = collection.find({'data': str(datetime.now().date())})
    horas = np.zeros(24).tolist()
    if results:
        for res in results:
            dt = dateHelper.str_date(date=res['data'], time=res['hora'])
            horas[dt.hour] += 1
    return 0, horas;


def grafico_dias():
    ym = str(datetime.now().date()).split('-')
    dias = np.zeros(int(ym[2])).tolist()
    ym = ym[0] + '-' + ym[1]
    results = collection.find({'data': {'$regex': ym}})
    if results:
        for res in results:
            dt = int(res['data'].split('-')[2])
            dias[dt - 1] += 1
    return 1, dias


def grafico_meses():
    ym = str(datetime.now().date()).split('-')
    meses = np.zeros(int(ym[1])).tolist()
    results = collection.find({'data': {'$regex': ym[0]}})
    if results:
        for res in results:
            dt = int(res['data'].split('-')[1])
            meses[dt - 1] += 1
    return 2, meses
