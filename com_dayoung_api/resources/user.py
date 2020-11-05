import os
import json
from flask import request
from flask_restful import Resource, reqparse
from com_dayoung_api.ext.db import db, openSession  # db 선택 Dayoungdb 에서
import pandas as pd
from com_dayoung_api.utils.file_helper import FileReader
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property


class UserPreprocess(object):
    """
    [This class is the main operator for user]

    Creates User Database with 7 columns.
    This enables user CRUD (Crete, Read, Update, Delete)
    Args:
        object ([object]): [description]
    """
    def __init__(self):
        """
        Creates fileReader object and sets the path to ""
        """
        self.fileReader = FileReader()
        self.path = os.path.abspath("")

    def hook(self):
        """
            Creates new model,
            for now it simply creates new_model which gets data from user.csv
        """
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


class UserDto(db.Model):  # 여기서 DB 모델 만든 것
    """
    [Creates User Model and corresponding table]
    """
    __tablename__ = 'users'  # 테이블 이름
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    # The __table_args__ attribute allows passing extra arguments to that Table

    # Creates table columns
    user_id: str = db.Column(db.String(30), primary_key=True, index=True)
    password: str = db.Column(db.String(30))
    fname: str = db.Column(db.String(30))
    lname: str = db.Column(db.String(30))
    age: int = db.Column(db.Integer)
    gender: str = db.Column(db.String(30))
    email: str = db.Column(db.String(80), unique=True)

    def __init__(self, user_id, password, fname, lname, age, gender, email):
        """
        Recives 7 parameters that are used to construct User Table
        user_id = 유저 고유 아이디 (Unique)
        password = 비밀번호
        fname = 성
        lname = 이름
        age = 나이
        gender = 성별
        email = 이메일 -> 나중에는 이메일이 아이디로 사용될 것 그래서 이것도 (Unique)
        """
        self.user_id = user_id
        self.password = password
        self.fname = fname
        self.lname = lname
        self.age = age
        self.gender = gender
        self.email = email

    @hybrid_property
    def fullname(self):
        """
        성과 이름을 합쳐서 풀네임을 만들어서 return 한다
        returns fullname
        """
        if self.fname is not None:
            return self.fname + " " + self.lname
        else:
            return self.lname
    # some_user = session.query(User).first()
    # print(s()ome_user.fullname)
    # as well as usable within queries:
    # some_user = session.query(User).filter(User.fullname == "John Smith").first

    def json(self):
        """
        UserDto (User 모델)이 주어지면 json file 로 리턴한다 
        """
        return {
            'user_id': self.user_id,
            'password': self.password,
            'lname': self.lname,
            'age': self.age,
            'fname': self.fname,
            'gender': self.gender,
            'email': self.email
        }

    def __str__(self):
        """
        User id 를 리턴한다
        """
        return self.user_id


class UserVo:
    """
    User model 에 쓸 parameter 들을 생성 시킨다.
    """
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
    """
        User 모델을 접근 하는 객체
        예: CRUD: (Create, Read, Update, Delete)
    """
    @staticmethod
    def bulk():
        """
        모든 유저 리스트를 DataBase 안에 넣어준다
        """
        df = user_preprocess.hook()
        print(df.head())
        session.bulk_insert_mappings(UserDto, df.to_dict(orient="records"))
        session.commit()
        session.close()

    @staticmethod
    def count():
        """
        데이터 베이스 안에 몇명의 유저들이 있는지
        숫자를 리턴한다
        """
        return session.query(func.count(UserDto.user_id)).one()

    @staticmethod
    def update(user):
        """
        유저 정보를 수정해 준다
        새로운 유저 정보를 가진 유저를 가져와 기존의
        유저 정보를 수정해 준다.

        Parameter: 새로운 유저 정보를 가진 유저
        """
        Session = openSession()
        session = Session()
        print(f"{user.lname}")
        print(f"{user.fname}")
        session.query(UserDto).filter(UserDto.user_id == user.user_id).update({UserDto.lname: user.lname,
                                                                               UserDto.fname: user.fname,
                                                                               UserDto.age: user.age,
                                                                               UserDto.password: user.password,
                                                                               UserDto.age: user.age,
                                                                               UserDto.email: user.email})
        session.commit()
        session.close()

    @staticmethod
    def register(user):
        """
        새로운 유저를 parameter 로 가져온다.
        새로운 유저를 데이터베이스 안에 넣는다.
        """
        db.session.add(user)
        db.session.commit()

    @classmethod
    def delete(cls, id):
        """
        유저의 id 정보 (user_id) 를 가져와
        해당 id를 가진 유저를 데이터베이스에서
        삭제 시켜준다.
        """
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()
        session.close()


    @classmethod
    def find_all(cls):
        """
        데이터 베이스 안에 있는 모든 유저 정보를 찾는다

        Returns:
            제이슨 형식으로 데이터를 리턴해준다.
        """
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))

    @classmethod
    def find_by_name(cls, name):
        """
        주어진 이름을 토대로 유저를 찾아서
        해당 정보를 리턴해준다.
        """
        return session.query(UserDto).filter(UserDto.fname.like(f'%{name}%'))

    @classmethod
    def find_by_id(cls, user_id):
        """
        주어진 아이디를 토대로 유저를 찾아서
        해당 정보를 리턴해준다.
        """
        return session.query(UserDto).filter(UserDto.user_id.like(f'{user_id}')).one()

    @classmethod
    def login(cls, user):
        """
        유저 정보를 받아와, 해당 유저가 데이터베이스에 있는지 확인.
        확인 후, 있으면 로그인 시켜준다.

        Parameter: 유저 모델을 받아온다
        return: 유저 정보를 리턴해준다.
        """
        print("----------------login")
        sql = cls.query\
            .filter(cls.user_id.like(user.user_id))\
            .filter(cls.password.like(user.password))
        print("login type ", type(sql))
        df = pd.read_sql(sql.statement, sql.session.bind)
        print(json.loads(df.to_json(orient='records')))
        return json.loads(df.to_json(orient='records'))


if __name__ == "__main__":
    """
    데이터 베이스에 모든 유저 정보들을 넣어준다.
    """
    UserDao.bulk()


class User(Resource):
    """
    서버와 정보를 주고 받는다.
    """
    @staticmethod
    def put(id: str):
        """
        서버에서 해당 ID 의 새로운 유저 정보를 받아온다.
        정보를 토대로 해당 ID 유저의 정보를 바꿔서
        정보를 서버에 보내준다.

        parameter: 유저 아이디를 받아온다
        return: 새로운 유저 데이터를 리턴 한다
        """
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        parser.add_argument('user_id', type=str, required=True,
                                                help='This field should be a user_id')
        parser.add_argument('password', type=str, required=True,
                                                help='This field should be a password')
        parser.add_argument('gender', type=str, required=True,
                                                help='This field should be a gender')
        parser.add_argument('lname', type=str, required=True,
                                                help='This field should be a lname')
        parser.add_argument('fname', type=str, required=True,
                                                help='This field should be a fname')
        parser.add_argument('email', type=str, required=True,
                                                help='This field should be a fname')
        parser.add_argument('age', type=int, required=True,
                                                help='This field should be a age')

        print("argument added")
        # def __init__(self, user_id, password,fname, lname, age, gender,email):
        args = parser.parse_args()
        print(f'User {args["user_id"]} updated')
        print(f'User {args["password"]} updated')
        user = UserDto(args.user_id, args.password, args.fname,
                       args.lname, args.age, args.gender, args.email)
        print("user created")
        UserDao.update(user)
        data = user.json()
        return data, 200

    @staticmethod
    def delete(id: str):
        """
        유저 아디를 받아와 해당 유저를 삭제한다.
        Parameter: 유저 아이디
        """
        UserDao.delete(id)
        print(f'User {id} Deleted')

    # @staticmethod
    # def post():
    #     """
    #     이거 아무것도 안하는데??
    #     """
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('user_id', type=str, required=True,
    #                                             help='This field should be a user_id')
    #     parser.add_argument('password', type=str, required=True,
    #                                             help='This field should be a password')
    #     args = parser.parse_args()
    #     print(f'User {args["id"]} added ')
    #     params = json.loads(request.get_data(), encoding='utf-8')
    #     if len(params) == 0:
    #         return 'No parameter'
    #     params_str = ''
    #     for key in params.keys():
    #         params_str += 'key: {}, value: {}<br>'.format(key, params[key])
    #     return {'code': 0, 'message': 'SUCCESS'}, 200

    @staticmethod
    def get(id: str):
        """
        유저 아이디를 받아와 해당 유저 객채를 리턴한다
        Parameter: User ID 를 받아온다
        return: 해당 아이디 유저 객채
        """
        print(f'::::::::::::: User {id} added ')
        try:
            user = UserDao.find_by_id(id)
            data = user.json()
            return data, 200
        except Exception as e:
            print(e)
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
    """
    서버와 정보를 주고 받는다.
    """
    @staticmethod
    def post():
        """
        모든 유저 정보를 데이터 베이스 안에 넣어준다
        """
        ud = UserDao()
        ud.bulk('users')

    @staticmethod
    def get():
        """
        데이터 베이스 안에 있는 모든 유저 정보를 찾아서 리턴해준다.
        """
        data = UserDao.find_all()
        print("list : ", type(data))
        return data, 200


class Auth(Resource):
    # self, user_id, password,fname, lname, age, gender,email
    @staticmethod
    def post():
        """
        유저 정보를 받아와 새로운 유저를 생성해 준다.
        """
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
        user = UserDto(args.user_id, args.password, args.fname, args.lname,
                       args.age, args.gender, args.email)

        print("아이디: ", user.user_id)
        print("비밀번호: ", user.password)
        print("이메일 :", user.email)
        print("성 :", user.lname)
        print("이름 :", user.fname)
        print("나이 :", user.age)
        print("성별 :", user.gender)
        try:
            UserDao.register(user)  # return 하긴 함
            return "worked"
        except Exception as e:
            return e


class Access(Resource):
    """
    서버와 정보를 주고 받는다.
    """
    @staticmethod
    def post():
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        parser.add_argument('user_id', type=str, required=True,
                                                help='This field should be a user_id')
        parser.add_argument('password', type=str, required=True,
                                                help='This field should be a password')
        args = parser.parse_args()
        print(args)
        user = UserVo()
        user.user_id = args.user_id
        user.password = args.password

        print("아이디: ", user.user_id)
        print("비밀번호: ", user.password)
        data = UserDao.login(user)
        return data[0], 200


class Delete(Resource):
    """
    정보를 받아와 유저 정보를 삭제 한다
    """
    @staticmethod
    def post(id: str):
        """
        Parameter: 유저 아이디를 받아온다.
        """
        UserDao.delete(id)
