from datetime import datetime
from helpers import dateHelper
import numpy as np
from PIL import Image as Img
from io import BytesIO
import base64


class DAO:

    def __init__(self, mongo):
        self.__collection = mongo.db.fotos

    def insert_fotos(self,imagem):
        data, hora = str(datetime.now()).split(' ')
        hora = hora.split('.')[0]
        #img = cv2.imencode('.jpeg', imagem)[1].tostring()
        buffer = BytesIO()
        pil_image = Img.fromarray(imagem, 'RGB')
        pil_image.save(buffer,format='PNG')
        img = buffer.getvalue()
        img64 = base64.b64encode(img).decode()
        local = 'casa'
        dicionario = {
            'imagem': img64,
            'data': data,
            'hora': hora,
            'local': local
        }
        #collection.insert_one(dicionario)
        return dicionario


    def grafico_horas(self):
        results = self.__collection.find({'data': str(datetime.now().date())})
        horas = np.zeros(datetime.now().hour).tolist()
        if results:
            for res in results:
                dt = dateHelper.str_date(date=res['data'], time=res['hora'])
                horas[dt.hour-1] += 1
        return 0, horas


    def grafico_dias(self):
        ym = str(datetime.now().date()).split('-')
        dias = np.zeros(int(ym[2])).tolist()
        ym = ym[0] + '-' + ym[1]
        results = self.__collection.find({'data': {'$regex': ym}})
        if results:
            for res in results:
                dt = int(res['data'].split('-')[2])
                dias[dt - 1] += 1
        return 1, dias


    def grafico_meses(self):
        ym = str(datetime.now().date()).split('-')
        meses = np.zeros(int(ym[1])).tolist()
        results = self.__collection.find({'data': {'$regex': ym[0]}})
        if results:
            for res in results:
                dt = int(res['data'].split('-')[1])
                meses[dt - 1] += 1
        return 2, meses
