from typing import List
from flask_restful import Resource, reqparse
from com_dayoung_api.actor.dao import ActorDao
from com_dayoung_api.actor.dto import ActorDto, ActorVo
import json
from flask import jsonify
from flask import request

parser = reqparse.RequestParser() # only allow price changes, no name changes allowed
parser.add_argument('actorid', type=str, required=True,
                                        help='This field should be a actorid')
# 여기 딴거 드거야 함 actor password 없음 id 만 있어도 될듯

class Actor(Resource):
    def __init__(self):
        print("지금 actor api 들어옴!!!!!")
        print()    
        print()    
        print()    
         
    @ staticmethod
    def post():
        print('Post entered')
        args = parser.parse_args()
        print(f'Actor {args["id"]} added ')
        params = json.loads(request.get_data(), encoding='utf-8')
        if len(params) == 0:
            return 'No parameter'

        params_str = ''
        for key in params.keys():
            params_str += 'key: {}, value: {}<br>'.format(key, params[key])
            return {'code':0, 'message': 'SUCCESS'}, 200

    
    @staticmethod
    def get(id):
        print(f'Actor {id} added')
        try:
            actor = ActorDao.find_by_id(id)
            if actor:
                return actor.json()
        except Exception as e:
            return {'message': 'Actor not found'}, 404

    @staticmethod
    def update():
        args = parser.parse_args()
        print(f'Actor {args["id"]} updated ')
        return {'code':0, 'message': 'Success'}, 200

    staticmethod
    def delete():
        args = parser.parse_args()
        print(f'Actor {args["id"]} deleted')
        return {'code' : 0, 'message' :'Success'}, 200

class Actors(Resource):
    
    def post(self):
        print("post 들어옴")
        ud = ActorDao()
        ud.insert_many('actors')

    def get(self):
        print('========== 10 ==========')
        data = ActorDao.find_all()
        return data, 200

class Auth(Resource):
    
    def post(self):
        
        body = request.get_json()
        actor = ActorDto(**body)
        ActorDao.save(actor)
        id = actor.actorid
        
        return {'id': str(id)}, 200 


class Access(Resource):
    def __init__(self):
        print("========5 actor/api.py Access")
    def post(self):
        print("========6 actor/api.py post")
        args = parser.parse_args() # 이걸 몰겠음
        print('---------------------------------7---------------------')
        actor = ActorVo()
        print('8 ---------------------------')
        actor.actorid = args.actorid
        actor.password = args.password
        print(actor.actorid)
        print(actor.password)
        data = ActorDao.login(actor)
        return data[0], 200
