# API nin yanıt verdiği, düşündüğü dosyalar resource klasörü altında yer almaktadır. 

from flask_restful import Resource, reqparse
from numpy import array
from optimization.genetic_algorithm_vrp import path

class Chat(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('fleet_size',
        type = int,
        required = True,
        help = "Filo sayısı boş bırakılamaz.")
    parser.add_argument('capacity',
        type = int,
        required = True,
        help = "Filo kapasitesi boş bırakılamaz.")
    parser.add_argument('coordinates',
        action='append',
        type = list,
        required = True,
        help = "Koordinat bilgisi boş bırakılamaz.")

    def post(self):
        data = Chat.parser.parse_args()
        # print(f"fleet_size: {data['fleet_size']}")
        # print(f"capacity: {data['fleet_size']}")
        # print(f"coordinates: {data['coordinates'][0]}")
        print(data)
        answers = path(data['fleet_size'],data['capacity'],data['coordinates'])
        result = {"response": answers["response"]}
        return result

