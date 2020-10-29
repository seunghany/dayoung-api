from typing import List
from flask import request
from flask_restful import Resource, reqparse
import json
from flask import jsonify
from com_dayoung_api.ext.db import db, openSession # db 선택 Dayoungdb 에서
import pandas as pd
import json
import os
from com_dayoung_api.utils.file_helper import FileReader
import pandas as pd
import numpy as np
from sqlalchemy import func
from pathlib import Path
from sqlalchemy.ext.hybrid import hybrid_property

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

class UserDto(db.Model): # 여기서 DB 모델 만든 것
    __tablename__ = 'users' # 테이블 이름
    __table_args__={'mysql_collate':'utf8_general_ci'}
    # The __table_args__ attribute allows passing extra arguments to that Table

    # Creates table columns
    user_id: str = db.Column(db.String(30), primary_key = True, index = True) 
    password: str = db.Column(db.String(30))
    fname: str = db.Column(db.String(30))
    lname: str = db.Column(db.String(30))
    age: int = db.Column(db.Integer)
    gender: str = db.Column(db.String(30))
    email: str = db.Column(db.String(80), unique=True)

    def __init__(self, user_id, password,fname, lname, age, gender,email):
        self.user_id = user_id
        self.password = password
        self.fname = fname
        self.lname = lname
        self.age = age
        self.gender = gender
        self.email = email

    @hybrid_property
    def fullname(self):
        
        if self.fname is not None:
            return self.fname + " " + self.lname
        else:
            return self.lname
    # some_user = session.query(User).first()
    # print(s()ome_user.fullname)
    # as well as usable within queries: 
    # some_user = session.query(User).filter(User.fullname == "John Smith").first
    
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
        
        

    def __str__(self):
         return self.user_id

class UserVo:
    user_id: str = ''
    password: str = ''
    lname: str = ''
    fname: str = ''
    gender: str = ''
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
    def update(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def register(user):
        Session = openSession()
        session = Session()
        print('I am at Register!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        db.session.add(user)
        print('I am at adddddddddddddddddddddddddddddd!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
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

    '''
    SELECT *
    FROM users
    WHERE user_name LIKE 'name'
    '''
    # the meaning of the symbol %
    # A% ==> Apple
    # %A ==> NA
    # %A% ==> Apple, NA, BAG 
    @classmethod
    def find_by_name(cls, name):
        return session.query(UserDto).filter(UserDto.fname.like(f'%{name}%'))

    '''
    SELECT *
    FROM users
    WHERE user_name LIKE 'a'
    '''
    # like() method itself produces the LIKE criteria 
    # for WHERE clause in the SELECT expression.
    @classmethod
    def find_by_id(cls, user_id):
        return session.query(UserDto).filter(UserDto.user_id.like(f'{user_id}')).one()

    @classmethod
    def login(cls, user):
        print("----------------login")
        sql = cls.query\
            .filter(cls.user_id.like(user.user_id))\
            .filter(cls.password.like(user.password))
        print("login type ",type(sql))
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


                                        

class User(Resource):

    @staticmethod
    def post():
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        parser.add_argument('user_id', type=str, required=True,
                                                help='This field should be a user_id')
        parser.add_argument('password', type=str, required=True,
                                                help='This field should be a password')
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
            data = user.json()
            return data, 200
        except Exception as e:
            print('failed')
            return {'message': 'User not found'}, 404

    # @staticmethod
    # def update():
    #     args = parser.parse_args()
    #     print(f'User {args["id"]} updated ')
    #     return {'code':0, 'message': 'SUCCESS'}, 200

    # @staticmethod
    # def delete():
    #     args = parser.parse_args()
    #     print(f'Us er {args["id"]} deleted')
    #     return {'code' : 0, 'message' : 'SUCCESS'}, 200    

class Users(Resource):
    @staticmethod
    def post():
        ud = UserDao()
        ud.bulk('users')
    @staticmethod
    def get():
        data = UserDao.find_all()
        print("list : ",type(data))
        return data, 200

class Auth(Resource):
    # self, user_id, password,fname, lname, age, gender,email
    @staticmethod
    def post():
        print("------------------여기는 user.py Auth ------------------- ")
        
        
       
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        parser.add_argument('user_id', type=str, required=True,
                                                help='This field should be a user_id')
        parser.add_argument('password', type=str, required=True,
                                                help='This field should be a password')
        parser.add_argument('gender', type=str, required=True,
                                                help='This field should be a gender')
        parser.add_argument('email', type=str, required=True,
                                                help='This field should be a email')
        parser.add_argument('lname', type=str, required=True,
                                                help='This field should be a lname')
        parser.add_argument('fname', type=str, required=True,
                                                help='This field should be a fname')
        parser.add_argument('age', type=int, required=True,
                                        help='This field should be a age')
        args = parser.parse_args()
        user = UserDto(args.user_id,args.password,args.fname,args.lname,args.age,args.gender,args.email)

        print("아이디: ", user.user_id)
        print("비밀번호: ", user.password)
        print("이메일 :", user.email )
        print("성 :", user.lname)
        print("이름 :", user.fname)
        print("나이 :", user.age)
        print("성별 :", user.gender)
        
        data = UserDao.register(user)
        return "worked"


class Access(Resource):
    @staticmethod
    def post():
        print('---------------------3---------------------')
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        parser.add_argument('user_id', type=str, required=True,
                                                help='This field should be a user_id')
        parser.add_argument('password', type=str, required=True,
                                                help='This field should be a password')

        args = parser.parse_args()

        print("-------------------444444")
        print(args)
        user = UserVo()
        user.user_id = args.user_id
        user.password = args.password
        
        print("아이디: ", user.user_id)
        print("비밀번호: ", user.password)
        data = UserDao.login(user)
        return data[0], 200
