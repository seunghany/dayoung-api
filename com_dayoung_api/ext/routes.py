# from com_dayoung_api.home.api import Home
# from com_dayoung_api.movie.api import Movie, Movies
# from com_dayoung_api.review.api import Review, Reviews
# from com_dayoung_api.user.api import User, Users, Auth, Access
import logging
from flask import Blueprint
from flask_restful import Api

from com_dayoung_api.resources.home import Home
from com_dayoung_api.resources.user import User, Users, Auth, Access
from com_dayoung_api.resources.actor import Actor, Actors
# from com_dayoung_api.resources.movie import Movie

# from com_dayoung_api.actor.api import Actor, Actors

home = Blueprint('home', __name__, url_prefix='/api')
user = Blueprint('user', __name__, url_prefix='/api/user')
users = Blueprint('users', __name__, url_prefix='/api/users')
auth = Blueprint('auth', __name__, url_prefix='/api/auth')
access = Blueprint('access', __name__, url_prefix='/api/access')
actor = Blueprint('actor', __name__, url_prefix='/api/actor')
actors = Blueprint('actors', __name__, url_prefix='/api/actors')
movie = Blueprint('movie', __name__, url_prefix='/api/movie')

print("hello world----------------------------")


# resful api 읽기

api = Api(home)
api = Api(user)
api = Api(users)
api = Api(auth)
api = Api(access)
api = Api(actor)
api = Api(actors)
api = Api(movie)

def initialize_routes(api):
    print("================ 2 route ====================")
    api.add_resource(Home, '/api')
    # api.add_resource(Movie, '/Movie/<string:id>')
    # api.add_resource(Movies, '/Movies')
    # api.add_resource(Review, '/Review<string:id>')
    # api.add_resource(Reviews, '/Reviews')
    api.add_resource(User, '/api/user/<string:id>')
    api.add_resource(Users, '/api/users')
    api.add_resource(Auth, '/api/auth')
    api.add_resource(Access, '/api/access')
    api.add_resource(Actor, '/api/actor/<string:id>')
    api.add_resource(Actors, '/api/actors')

    
    
@user.errorhandler(500)
def user_api_error(e):
    logging.exception('An error occurred during user request. %s' % str(e))
    return 'An internal error occurred.', 500

@home.errorhandler(500)
def home_api_error(e):
    logging.exception('An error occurred during home request. %s' % str(e))
    return 'An internal error occurred.', 500

@actor.errorhandler(500)
def actor_api_error(e):
    logging.exception('An error occurred during actor request. %s' % str(e))
    return 'An internal error occurred.', 500
