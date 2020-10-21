from com_dayoung_api.ext.db import db
from com_dayoung_api.actor.pro import ActorPro
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

class ActorDto(db.Model):
    __tablename__ = 'actors'
    __table_args__={'mysql_collate':'utf8_general_ci'}
    # columns=['photo_url', 'age','name','real_name','religion','agency', 'spouse', 'children','debut_year','actor_id']
    actorid = str = db.Column(db.String(30), primary_key = True, index = True)
    photo_url: str = db.Column(db.String(100))
    name: str = db.Column(db.String(30))
    age: str = db.Column(db.String(30))
    real_name: str = db.Column(db.String(30))
    religion: str = db.Column(db.String(30))
    agency: str = db.Column(db.String(30))
    spouse: str = db.Column(db.String(30))
    children: str = db.Column(db.Integer)
    debut_year: int = db.Column(db.Integer)

    def __init__(self, photo_url, actorid, name, age, real_name, spouse, children, debut_year, agency, religion):
        self.photo_url = photo_url
        self.actorid = actorid
        self.name = name
        self.age = age
        self.real_name = real_name
        self.religion = religion
        self.agency = agency
        self.spouse = spouse
        self.children = children
        self.debut_year = debut_year

    # def __repr__(self):
    #     return f'Actors(id={self.id}, user={self.userid}, \
    #             password={self.password}, name={self.name})'

    
    @property
    def json(self):
        return {
            'photo_url' : self.photo_url,
            'actorId' : self.actorid,
            'name' : self.name,
            'age' : self.age,
            'real_name' : self.real_name,
            'spouse' : self.spouse,
            'children' : self.children,
            'debut_year' : self.debut_year,
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
charset = {'utf8':'utf8'}
url = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset=utf8"
engine = create_engine(url)
service = ActorPro()
Session = sessionmaker(bind=engine)
s = Session()
df = service.hook()
print(df.head())
s.bulk_insert_mappings(ActorDto, df.to_dict(orient="records"))
s.commit()
s.close()