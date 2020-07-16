from flask_pymongo import pymongo
from datetime import datetime
import cv2
import base64

CONNECTION_STRING = "mongodb+srv://admin:123@ipkiss.bcenh.gcp.mongodb.net/cv?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('cv')
fotos = pymongo.collection.Collection(db,'fotos')
def insert_fotos(imagem):
    data, hora = str(datetime.now()).split(' ')
    img = cv2.imencode('.jpeg', imagem)[1].tostring()
    img64 = base64.b64encode(img).decode()
    local = 'casa'
    dicionario  = {
        'imagem': img64,
        'data': data,
        'hora': hora,
        'local': local
    }
    #print(img64)
    fotos.insert_one(dicionario)



