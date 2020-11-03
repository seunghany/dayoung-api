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
        
        actors_name = ['전지현', "이병한", "손예진"]
        actors_name = ['전지현']
        actors_name =["수지", "이병헌","한지민", "전지현","손예진","안소희","강동원",
                        "하정우","김혜수","현빈" ,"송강호", "이나영", "신민아" ]
        
        self.crawl = Crawling(actors_name) # 이병헌 is given as default
        # print(self.dataFrame)
        
    def hook(self):
        self.dataFrame = self.crawl.crawl()
        print(self.dataFrame)
        return self.dataFrame

class ActorDto(db.Model):
    __tablename__ = 'actors'
    __table_args__={'mysql_collate':'utf8_general_ci'}
    # columns=['photoUrl', 'age','name','realName','religion','agency', 'spouse', 'children','debutYear','actor_id']
    actor_id: str = db.Column(db.String(30), primary_key = True, index = True)
    photo_url: str = db.Column(db.String(200))
    name: str = db.Column(db.String(30))
    age: str = db.Column(db.String(30))
    real_name: str = db.Column(db.String(30))
    religion: str = db.Column(db.String(30))
    agency: str = db.Column(db.String(30))
    spouse: str = db.Column(db.String(30))
    children: str = db.Column(db.String(30))
    debut_year: int = db.Column(db.Integer)

    def __init__(self, photo_url, actor_id, name, age, real_name, spouse, children, debut_year, agency, religion):
        self.photo_url = photo_url
        self.actor_id = actor_id
        self.name = name
        self.age = age
        self.real_name = real_name
        self.religion = religion
        self.agency = agency
        self.spouse = spouse
        self.children = children
        self.debut_year = debut_year

    def json(self):
        return {
            'photo_url' : self.photo_url,
            'actor_id' : self.actor_id,
            'name' : self.name,
            'age' : self.age,
            'real_name' : self.real_name,
            'spouse' : self.spouse,
            'children' : self.children,
            'debut_year' : self.debut_year,
            'religion' : self.religion,
            'agency' : self.agency
        }

class ActorVo:
    actor_id: str = ''
    photo_url: str = ''
    age: str = ''
    name: str = ''
    real_name: str = ''
    religion: str = ''
    agency: str = ''
    spouse: str = ''
    children: str = ''
    debut_year: int = 0

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
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()

    @classmethod
    def find_all(cls):
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filer_by(name == name)

    @classmethod
    def find_by_id(cls, actor_id):
        return session.query(ActorDto).filter(ActorDto.actor_id.like(f'{actor_id}')).one()


    @classmethod
    def login(cls, actor):
        sql = cls.query\
            .filter(cls.actor_id.like(actor.actor_id))\
            .filter(cls.password.like(actor.password))
        df = pd.read_sql(sql.statement, sql.session.bind)
        print(json.loads(df.to_json(orient='records')))
        return json.loads(df.to_json(orient='records'))

    @classmethod
    def delete_actor(cls,id):
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()
        session.close()


if __name__ == "__main__":
    ActorDao.bulk()



# ==============================================================
# ==============================================================
# ==============================================================
# ==============================================================
# ==============================================================


parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
parser.add_argument('actorId', type=str, required=True,
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
        ActorDao.delete_actor(id)
        print(f'Actor {id} deleted')
        return {'code' : 0, 'message' : 'SUCCESS'}, 200    

class Actors(Resource):
    @staticmethod
    def post():
        ud = ActorDao()
        ud.bulk('actors')
    @staticmethod
    def get():
        data = ActorDao.find_all()
        return data, 200

class Auth(Resource):
    @staticmethod
    def post():
        body = request.get_json()
        actor = ActorDto(**body)
        ActorDao.save(actor)
        id = actor.actor_id
        return {'id': str(id)}, 200 


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