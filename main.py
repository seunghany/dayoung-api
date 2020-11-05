"""
This is main file

Creates table for use and connects database to SQLALCHEMY

"""

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from com_dayoung_api.ext.db import url, db
from com_dayoung_api.ext.routes import initialize_routes
from com_dayoung_api.resources.user import UserDao
from com_dayoung_api.resources.actor import ActorDao


app = Flask(__name__)
CORS(app, resources={r'/api/*': {"origins": "*"}}) # api open subdomain

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)
with app.app_context():
    db.create_all()
    user_count = UserDao.count()
    print(f'***** Users Total Count is {user_count} *****')
    if user_count[0] == 0:
        UserDao.bulk()

    actor_count = ActorDao.count()
    print(f'***** Actors Total Count is {actor_count} *****')
    if actor_count[0] == 0:
        ActorDao.bulk()

initialize_routes(api)
