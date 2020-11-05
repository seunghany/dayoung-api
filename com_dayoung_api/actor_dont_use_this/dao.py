from com_dayoung_api.ext.db import db, openSession
from com_dayoung_api.actor.service import ActorService
from com_dayoung_api.actor.dto import ActorDto
import pandas as pd
import json

class ActorDao(ActorDto):

    @classmethod
    def find_all(cls):
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filer_by(name == name).all()

    @classmethod
    def find_by_id(cls, actorid):
        return cls.query.filter_by(actorid == actorid).first()

    @classmethod
    def login(cls, actor):
        sql = cls.query\
            .filter(cls.actorid.like(actor.actorid))\
            .filter(cls.password.like(actor.password))
        df = pd.read_sql(sql.statement, sql.session.bind)
        print('==================================')
        print(json.loads(df.to_json(orient='records')))
        return json.loads(df.to_json(orient='records'))
            

    @staticmethod
    def save(actor):
        db.session.add(actor)
        db.session.commit()

    @staticmethod   
    def insert_many():
        service = ActorService()
        Session = openSession()
        session = Session()
        df = service.hook()
        print(df.head())
        session.bulk_insert_mappings(ActorDto, df.to_dict(orient="records"))
        session.commit()
        session.close()

    @staticmethod
    def modify_actor(actor):
        db.session.add(actor)
        db.session.commit()

    @classmethod
    def delete_actor(cls,id):
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()