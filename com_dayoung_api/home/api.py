from com_dayoung_api.ext.db import config
from flask_restful import Resource

class Home(Resource):
    def get(self):
        return {'message': 'Server Start'}
