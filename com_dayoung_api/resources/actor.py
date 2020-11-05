from typing import List
from flask import request
from flask_restful import Resource, reqparse
import json
from flask import jsonify
from com_dayoung_api.ext.db import db, openSession
import pandas as pd
import json
import os
from com_dayoung_api.utils.file_helper import FileReader
import pandas as pd
import numpy as np
from sqlalchemy import func
from pathlib import Path

from com_dayoung_api.resources.crawling import Crawling

class ActorPreprocess(object):
    
    def __init__(self):
        self.c = Crawling() # 이병헌 is given as default
        
        # print(self.dataFrame)
        
    def hook(self):
        dataFrame = self.c.crawl()
        # print(dataFrame)
        return dataFrame

class ActorDto(db.Model):
    __tablename__ = 'actors'
    __table_args__={'mysql_collate':'utf8_general_ci'}
    # 'photoUrl', 'age', 'actor_id', 'name', 'realName', 'religion', 'agency', 'spouse', 'children', 'debutYear', 'gender'

    # columns=['photoUrl', 'age','name','realName','religion','agency', 'spouse', 'children','debutYear','actor_id']
    actor_id: str = db.Column(db.String(30), primary_key = True, index = True)
    name: str = db.Column(db.String(30))
    gender: str = db.Column(db.String(1))
    age: str = db.Column(db.String(30))
    real_name: str = db.Column(db.String(30))
    religion: str = db.Column(db.String(30))
    agency: str = db.Column(db.String(30))
    spouse: str = db.Column(db.String(30))
    children: str = db.Column(db.String(100))
    debut_year: int = db.Column(db.Integer)
    state: str = db.Column(db.String(1))
    photo_url: str = db.Column(db.String(200))

    def __init__(self, photo_url, actor_id, name, gender, age, real_name, spouse, children, debut_year, agency, religion, state):
        self.photo_url = photo_url
        self.actor_id = actor_id
        self.name = name
        self.gender = gender
        self.age = age
        self.real_name = real_name
        self.religion = religion
        self.agency = agency
        self.spouse = spouse
        self.children = children
        self.debut_year = debut_year
        self.state = state

    def json(self):
        return {
            'photo_url' : self.photo_url,
            'actor_id' : self.actor_id,
            'name' : self.name,
            'gender' : self.gender,
            'age' : self.age,
            'real_name' : self.real_name,
            'spouse' : self.spouse,
            'children' : self.children,
            'debut_year' : self.debut_year,
            'religion' : self.religion,
            'agency' : self.agency,
            'state' : self.state
        }

class ActorVo:
    actor_id: str = ''
    photo_url: str = ''
    gender: str = ''
    age: str = ''
    name: str = ''
    real_name: str = ''
    religion: str = ''
    agency: str = ''
    spouse: str = ''
    children: str = ''
    debut_year: int = 0
    state: str = '0'

Session = openSession()
session = Session()
actor_preprocess = ActorPreprocess()
    
    
"""   
# ==============================================================
# ==============================================================
# ====================     Preprocess  ============================
# ==============================================================
# ==============================================================
"""



# ==============================================================
# ==============================================================
# =================     Controller  ============================
# ==============================================================
# ==============================================================

parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
parser.add_argument('actor_id', type=str, required=True,
                                        help='This field should be a actor_id')


class ActorDao(ActorDto):
    
    @staticmethod   
    def add(actor_name):
        crawl = Crawling(actor_name)
        df = crawl.crawl()
        actor = df.to_dict(orient="records")
        actor = actor[0]
        actor = ActorDto(**actor)
        
        # print("_________________________________________________________________")

        # print("actor 타입 ", type(actor))
        # print(actor['age'])
        # print("여기 옴222222222222222222222?")
        # actor = ActorDto(actor)
        # print("actor 타입 ", type(actor))
        Session = openSession()
        session = Session()
        print("--------------------------------------------------------------------------")
        db.session.add(actor)
        db.session.commit()
        session.close()


    def bulk():
        df = actor_preprocess.hook()
        print(df.head())
        session.bulk_insert_mappings(ActorDto, df.to_dict(orient="records"))
        session.commit()
        session.close()

    @staticmethod
    def count():
        return session.query(func.count(ActorDto.actor_id)).one()

    @staticmethod
    def save(actor):
        db.session.add(actor)
        db.session.commit()

    @staticmethod
    def update(actor):
        db.session.add(actor)
        db.session.commit()

    @classmethod
    def delete(cls,id):
        # this deletes actor from the whole database
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()
        session.close()

    @classmethod
    def find_all(cls):
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))
    
    @classmethod
    def find_state_one(cls):
        return session.query(ActorDto).filter(ActorDto.state.like("1")).all()
        
        # session.query(ActorDto).filter(ActorDto.state.like("1")).all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filer_by(name == name)

    @classmethod
    def find_by_id(cls, actor_id):
        return session.query(ActorDto).filter(ActorDto.actor_id.like(f'{actor_id}')).one()

    @classmethod
    def find_id_by_name(cls,name):
        return session.query(ActorDto).filter(ActorDto.name.like(f'{name}')).one()


    @classmethod
    def login(cls, actor):
        sql = cls.query\
            .filter(cls.actor_id.like(actor.actor_id))\
            .filter(cls.password.like(actor.password))
        df = pd.read_sql(sql.statement, sql.session.bind)
        print(json.loads(df.to_json(orient='records')))
        return json.loads(df.to_json(orient='records'))

    @classmethod
    def delete_actor_by_setting_state_to_one(cls,id):
        # This does not delete Actor from the database but rather simply updates 
        # actor column "state" to 0 which will hide its display from the user 
        # where as user will think that the selected actor has been deleted
        session.query(ActorDto).filter(ActorDto.actor_id == id).update({ActorDto.state:"0"}, synchronize_session=False)
        session.commit()
        session.close()
    
    @classmethod
    def add_actor_by_setting_state_to_one(cls,id):
        session.query(ActorDto).filter(ActorDto.actor_id == id).update({ActorDto.state:"1"}, synchronize_session=False)
        session.commit()
        session.close()



if __name__ == "__main__":
    ActorDao.bulk()



# ==============================================================
# ==============================================================
# ==============================================================
# ==============================================================
# ==============================================================


parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
parser.add_argument('actor_id', type=str, required=True,
                                        help='This field should be a actorId')
parser.add_argument('password', type=str, required=True,
                                        help='This field should be a password')

class Actor(Resource):
    @staticmethod
    def post():
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
    def get(id: str):
        print(f'Actor {id} added ')
        try:
            actor = ActorDao.find_by_id(id)
            data = actor.json()
            
            return data, 200
        except Exception as e:
            return {'message': 'Actor not found'}, 404

    @staticmethod
    def update():
        args = parser.parse_args()
        print(f'Actor {args["id"]} updated ')
        return {'code':0, 'message': 'SUCCESS'}, 200

    @staticmethod
    def delete(id):
        print("-------------------------------")
        print("-------------------------------")
        print("-------------------------------")
        print("-------------------------------")
        ActorDao.delete_actor_by_setting_state_to_one(id)
        print(f'Actor {id} deleted')
        return {'code' : 0, 'message' : 'SUCCESS'}, 200    

class Actors(Resource):
    @staticmethod
    def post():
        ud = ActorDao()
        ud.bulk('actors')
    @staticmethod
    def get():
        # find all 하지 말고
        # state 가 1 인 것만!
        # data = ActorDao.find_all()
        actors = ActorDao.find_state_one()
        # 여기서 이제 review를 제이슨화 시킨후 보내주면 됨
        data = []
        for actor in actors:
            data.append(actor.json())
        return data[:]


class Access(Resource):
    @staticmethod
    def post():
        args = parser.parse_args()
        actor = ActorVo()
        actor.actor_id = args.actorId
        actor.password = args.password
        print(actor.actor_id)
        print(actor.password)
        data = ActorDao.login(actor)
        return data[0], 200

class Auth(Resource):
    @staticmethod
    def post():
        body = request.get_json()
        actor = ActorDto(**body)
        ActorDao.save(actor)
        id = actor.actor_id
        return {'id': str(id)}, 200 

class AddActor(Resource):
    @staticmethod
    def post(name):
        id = ActorDao.find_id_by_name(name)
        ActorDao.add_actor_by_setting_state_to_one(id)
        print(f'Actor {name} added')
        return {'code' : 0, 'message' : 'SUCCESS'}, 200   
        