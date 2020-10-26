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

class UserDto(db.Model):
    __tablename__ = 'users'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    userid: str = db.Column(db.String(30), primary_key = True, index = True)
    password: str = db.Column(db.String(30))
    lname: str = db.Column(db.String(30))
    age: int = db.Column(db.Integer)
    fname: str = db.Column(db.String(30))
    gender: str = db.Column(db.String(30))
    email: str = db.Column(db.String(60))

    def __init__(self, userid, password, lname, age, fname, gender,email):
        self.userid = userid
        self.password = password
        self.lname = lname
        self.age = age
        self.fname = fname
        self.gender = gender
        self.email = email



    @property
    def json(self):
        return {
            'userid' : self.userid,
            'password' : self.password,
            'lname' : self.lname,
            'age' : self.age,
            'fname' : self.fname,
            'gender': self.gender,
            'email': self.email
        }

class UserVo:
    userid: str = ''
    password: str = ''
    lname: str = ''
    fname: str = ''
    gender: str = 0
    age: int = 0
    email: str = ''

class UserDao(UserDto):
    @classmethod
    def count(cls):
        return cls.query.count()
    
    @classmethod
    def find_all(cls):
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filer_by(name == name)

    @classmethod
    def find_by_id(cls, userid):
        return cls.query.filter_by(userid == userid)


    @classmethod
    def login(cls, user):
        sql = cls.query\
            .filter(cls.userid.like(user.userid))\
            .filter(cls.password.like(user.password))
        df = pd.read_sql(sql.statement, sql.session.bind)
        print(json.loads(df.to_json(orient='records')))
        return json.loads(df.to_json(orient='records'))
            

    @staticmethod
    def save(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod   
    def insert_many():
        service = UserService()
        Session = openSession()
        session = Session()
        df = service.hook()
        print(df.head())
        session.bulk_insert_mappings(UserDto, df.to_dict(orient="records"))
        session.commit()
        session.close()

    @staticmethod
    def modify_user(user):
        db.session.add(user)
        db.session.commit()

    @classmethod
    def delete_user(cls,id):
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()
        
"""   
# ==============================================================
# ==============================================================
# ====================     Service  ============================
# ==============================================================
# ==============================================================
"""

class UserService:
    def __init__(self):
        self.fileReader = FileReader()  
        self.path = os.path.abspath("")
        self.odf = None
    def hook(self):
        data = self.new_model()
        print(data)
        return data
    def new_model(self) -> object:
        path = os.path.abspath("")
        # \com_dayoung_api\
        fname = r"\data\user.csv"
        data = pd.read_csv(path + fname, encoding='utf-8')
        # print('***********')
        # data = data.head()
        # print(data)
        return data

if __name__ == '__main__':
    m = UserService()
    m.hook()

# ==============================================================
# ==============================================================
# =================     Controller  ============================
# ==============================================================
# ==============================================================

parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
parser.add_argument('userid', type=str, required=True,
                                        help='This field should be a userid')
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
    def get(id):
        print(f'User {id} added ')
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
    
    def post(self):
        ud = UserDao()
        ud.insert_many('users')

    def get(self):
        data = UserDao.find_all()
        return data, 200

class Auth(Resource):

    def post(self):
        body = request.get_json()
        user = UserDto(**body)
        UserDao.save(user)
        id = user.userid
        
        return {'id': str(id)}, 200 


class Access(Resource):
    
    def post(self):
        args = parser.parse_args()
        user = UserVo()
        user.userid = args.userid
        user.password = args.password
        print(user.userid)
        print(user.password)
        data = UserDao.login(user)
        return data[0], 200