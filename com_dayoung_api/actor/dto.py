from com_dayoung_api.ext.db import db
from com_dayoung_api.actor.service import ActorService
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

class ActorDto(db.Model):
    __tablename__ = 'actors'
    __table_args__={'mysql_collate':'utf8_general_ci'}
    # columns=['photoUrl', 'age','name','realName','religion','agency', 'spouse', 'children','debutYear','actorid']
    actorid: str = db.Column(db.String(30), primary_key = True, index = True)
    photoUrl: str = db.Column(db.String(200))
    name: str = db.Column(db.String(30))
    age: str = db.Column(db.String(30))
    realName: str = db.Column(db.String(30))
    religion: str = db.Column(db.String(30))
    agency: str = db.Column(db.String(30))
    spouse: str = db.Column(db.String(30))
    children: str = db.Column(db.String(30))
    debutYear: int = db.Column(db.Integer)

    def __init__(self, photoUrl, actorid, name, age, realName, spouse, children, debutYear, agency, religion):
        self.photoUrl = photoUrl
        self.actorid = actorid
        self.name = name
        self.age = age
        self.realName = realName
        self.religion = religion
        self.agency = agency
        self.spouse = spouse
        self.children = children
        self.debutYear = debutYear

    # def __repr__(self):
    #     return f'Actors(id={self.id}, user={self.userid}, \
    #             password={self.password}, name={self.name})'

    
    @property
    def json(self):
        return {
            'photoUrl' : self.photoUrl,
            'actorid' : self.actorid,
            'name' : self.name,
            'age' : self.age,
            'realName' : self.realName,
            'spouse' : self.spouse,
            'children' : self.children,
            'debutYear' : self.debutYear,
            'religion' : self.religion,
            'agency' : self.agency
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
    # columns=['photoUrl', 'age','name','realName','religion','agency', 'spouse', 'children','debutYear','actorid']
class ActorVo:
    actorid: str = ''
    photoUrl: str = ''
    age: str = ''
    name: str = ''
    realName: str = ''
    religion: str = ''
    agency: str = ''
    spouse: str = ''
    children: str = ''
    debutYear: int = 0
# charset = {'utf8':'utf8'}
# url = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset=utf8"
# engine = create_engine(url)
# service = ActorPro()
# Session = sessionmaker(bind=engine)
# s = Session()
# df = service.hook()
# print(df.head())
# s.bulk_insert_mappings(ActorDto, df.to_dict(orient="records"))
# s.commit()
# s.close()