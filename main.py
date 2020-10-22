from flask import Flask
from flask_restful import Api
from com_dayoung_api.ext.db import url, db
from com_dayoung_api.ext.routes import initialize_routes

from com_dayoung_api.movie.api import Movie, Movies
from com_dayoung_api.review.api import Review, Reviews
from com_dayoung_api.user.api import User, Users
from com_dayoung_api.actor.api import Actor, Actors
from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
print('========== url ==========')
print(url)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

initialize_routes(api)

with app.app_context():
    db.create_all()

@app.route('/api/test')
def test():
    return {'test', "Success"}
