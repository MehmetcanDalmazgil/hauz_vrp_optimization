from flask import Flask, jsonify
from flask.helpers import send_from_directory
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin

from resources.chat import Chat

app = Flask(__name__)
CORS(app, origins="*")
api = Api(app) # API metodlarını kullanmamızı kolay hale getirecek.

api.add_resource(Chat,'/vrp')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug = True)