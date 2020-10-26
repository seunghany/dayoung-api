from flask import Flask
from flask_restful import Api
from com_dayoung_api.ext.db import url, db
from com_dayoung_api.ext.routes import initialize_routes
from com_dayoung_api.resources.user import UserDao
from flask_cors import CORS
# from com_dayoung_api.movie.api import Movie, Movies
# from com_dayoung_api.review.api import Review, Reviews
# from com_dayoung_api.user.api import User, Users
# from com_dayoung_api.actor.api import Actor, Actors
# from com_dayoung_api.user import user


print('========== main 1 ==========')
app = Flask(__name__)
CORS(app, resources={r'/api/*': {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)
with app.app_context():
    db.create_all()
with app.app_context():
    count = UserDao.count()
    print(f'Users Total Count is {count}')
    if count == 0:
        UserDao.insert_many()

initialize_routes(api)
