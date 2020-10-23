from com_dayoung_api.ext.db import db
from com_dayoung_api.user.pro import UserPro
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

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

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit

config = {
    'user' : 'root',
    'password' : 'root',
    'host': '127.0.0.1',
    'port' : '3306',
    'database' : 'dayoungdb'
}
# charset = {'utf8':'utf8'}
# url = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset=utf8"
# engine = create_engine(url)
# service = UserPro()
# Session = sessionmaker(bind=engine)
# s = Session()
# df = service.hook()
# print(df.head())
# s.bulk_insert_mappings(UserDto, df.to_dict(orient="records"))
# s.commit()
# s.close()