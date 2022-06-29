# API nin yanıt verdiği, düşündüğü dosyalar resource klasörü altında yer almaktadır. 

import json

from flask_restful import Resource, reqparse
from numpy import array
from optimization.genetic_algorithm_vrp import path

class VRP(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('parameters',
        type = dict,
        required = True,
        help = "Mesaj alani bos birakilamaz!")
    parser.add_argument('orders',
        action='append',
        type = dict,
        required = True,
        help = "Mesaj alani bos birakilamaz!")

    def post(self):
        data = VRP.parser.parse_args()
        # print(f"fleet_size: {data['fleet_size']}")
        # print(f"capacity: {data['fleet_size']}")
        # print(f"coordinates: {data['coordinates'][0]}")
        coordinates = []
        order_id = []
        for i in range(0,len(data["orders"])):
            coordinates.append([data["orders"][i]["latitude"], data["orders"][i]["longitude"]])
            order_id.append(data["orders"][i]["ord_id"])
        
        print(order_id)
        answers = path(data["parameters"]["fleet_size"],data["parameters"]["capacity"], coordinates, order_id)
        # result = {"routes": answers["routes"]}
        # jsonString = json.dumps(answers)
        # jsonFile = open("data.json", "w")
        # jsonFile.write(jsonString)
        # jsonFile.close()
        return answers

