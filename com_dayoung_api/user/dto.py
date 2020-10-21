from com_dayoung_api.ext.db import db
from com_dayoung_api.user.pro import UserPro
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

class UserDto(db.Model):
    __tablename__ = 'users'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    userid: str = db.Column(db.String(30), primary_key = True, index = True)
    password: str = db.Column(db.String(30))
    name: str = db.Column(db.String(30))
    age: int = db.Column(db.Integer)
    date_of_birth: str = db.Column(db.String(30))
    gender: str = db.Column(db.String(30))

    def __init__(self, userid, password, name, age, date_of_birth, gender):
        self.userid = userid
        self.password = password
        self.name = name
        self.age = age
        self.date_of_birth = date_of_birth
        self.gender = gender



    @property
    def json(self):
        return {
            'userid' : self.userid,
            'password' : self.password,
            'name' : self.name,
            'age' : self.age,
            'date_of_birth' : self.date_of_birth,
            'gender': self.gender
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit

# config = {
#     'user' : 'root',
#     'password' : 'root',
#     'host': '127.0.0.1',
#     'port' : '3306',
#     'database' : 'dayoungdb'
# }
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