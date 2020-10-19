from com_dayoung_api.ext.db import db

class ActorDto(db.Model):
    __tablename__ = 'actors'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    actorid = str = db.Column(db.String(30), primary_key = True, index = True)
    name: str = db.Column(db.String(30))
    age: str = db.Column(db.String(30))
    real_name: str = db.Column(db.String(30))
    spouse: str = db.Column(db.String(30))
    children: str = db.Column(db.Integer)
    debut_year: int = db.Column(db.Integer)

    def __init__(self, actorId, name, age, real_name, spouse, children, debut_year):
        self.actorId = actorId
        self.name = name
        self.age = age
        self.real_name = real_name
        self.spouse = spouse
        self.children = children
        self.debut_year = debut_year

    def __repr__(self):
        return f'Actors(id={self.id}, user={self.userid}, \
                password={self.password}, name={self.name})'

    
    # 소속사 추가
    # 
    @property
    def json(self):
        return {
            'actorId' : self.actorId,
            'name' : self.name,
            'age' : self.age,
            'real_name' : self.real_name,
            'spouse' : self.spouse,
            'children' : self.children,
            'debut_year' : self.debut_year
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit