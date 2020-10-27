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

class UserPreprocess(object):
    def __init__(self):
        self.fileReader = FileReader()  
        self.path = os.path.abspath("")
    def hook(self):
        data = self.new_model()
        print(data)
        return data
    def new_model(self) -> object:
        path = os.path.abspath("")
        # \com_dayoung_api\
        fname = r"\com_dayoung_api\resources\data\user.csv"
        data = pd.read_csv(path + fname, encoding='utf-8')
        # print('***********')
        # data = data.head()
        # print(data)
        return data

# if __name__ == '__main__':
#     m = UserPreprocess()
#     m.hook()

class UserDto(db.Model):
    __tablename__ = 'users'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    user_id: str = db.Column(db.String(30), primary_key = True, index = True)
    password: str = db.Column(db.String(30))
    fname: str = db.Column(db.String(30))
    lname: str = db.Column(db.String(30))
    age: int = db.Column(db.Integer)
    gender: str = db.Column(db.String(30))
    email: str = db.Column(db.String(60))

    def __init__(self, user_id, password,fname, lname, age, gender,email):
        self.user_id = user_id
        self.password = password
        self.fname = fname
        self.lname = lname
        self.age = age
        self.gender = gender
        self.email = email



    @property
    def json(self):
        return {
            'user_id' : self.user_id,
            'password' : self.password,
            'lname' : self.lname,
            'age' : self.age,
            'fname' : self.fname,
            'gender': self.gender,
            'email': self.email
        }

class UserVo:
    user_id: str = ''
    password: str = ''
    lname: str = ''
    fname: str = ''
    gender: str = 0
    age: int = 0
    email: str = ''

Session = openSession()
session = Session()
user_preprocess = UserPreprocess()

class UserDao(UserDto):
    @staticmethod   
    def bulk():
        df = user_preprocess.hook()
        print(df.head())
        session.bulk_insert_mappings(UserDto, df.to_dict(orient="records"))
        session.commit()
        session.close()

    @staticmethod
    def count():
        return session.query(func.count(UserDto.user_id)).one()

    @staticmethod
    def save(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def update(user):
        db.session.add(user)
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
    def find_by_id(cls, user_id):
        return cls.query.filter_by(user_id == user_id)


    @classmethod
    def login(cls, user):
        sql = cls.query\
            .filter(cls.user_id.like(user.user_id))\
            .filter(cls.password.like(user.password))
        df = pd.read_sql(sql.statement, sql.session.bind)
        print(json.loads(df.to_json(orient='records')))
        return json.loads(df.to_json(orient='records'))
            


if __name__ == "__main__":
    UserDao.bulk()
        
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
parser.add_argument('user_id', type=str, required=True,
                                        help='This field should be a user_id')
parser.add_argument('password', type=str, required=True,
                                        help='This field should be a password')

class User(Resource):
    @staticmethod
    def post():
        args = parser.parse_args()
        print(f'User {args["id"]} added ')
        params = json.loads(request.get_data(), encoding='utf-8')
        if len(params) == 0:

            return 'No parameter'

        params_str = ''
        for key in params.keys():
            params_str += 'key: {}, value: {}<br>'.format(key, params[key])
        return {'code':0, 'message': 'SUCCESS'}, 200
    @staticmethod
    def get(id: str):
        print(f'::::::::::::: User {id} added ')
        try:
            user = UserDao.find_by_id(id)
            if user:
                return user.json()
        except Exception as e:
            return {'message': 'User not found'}, 404

    @staticmethod
    def update():
        args = parser.parse_args()
        print(f'User {args["id"]} updated ')
        return {'code':0, 'message': 'SUCCESS'}, 200

    @staticmethod
    def delete():
        args = parser.parse_args()
        print(f'USer {args["id"]} deleted')
        return {'code' : 0, 'message' : 'SUCCESS'}, 200    

class Users(Resource):
    @staticmethod
    def post():
        ud = UserDao()
        ud.bulk('users')
    @staticmethod
    def get():
        data = UserDao.find_all()
        return data, 200

class Auth(Resource):
    @staticmethod
    def post():
        body = request.get_json()
        user = UserDto(**body)
        UserDao.save(user)
        id = user.user_id
        
        return {'id': str(id)}, 200 


class Access(Resource):
    @staticmethod
    def post():
        args = parser.parse_args()
        user = UserVo()
        user.user_id = args.user_id
        user.password = args.password
        print(user.user_id)
        print(user.password)
        data = UserDao.login(user)
        return data[0], 200
