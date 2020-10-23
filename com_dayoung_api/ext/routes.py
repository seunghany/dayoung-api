from com_dayoung_api.home.api import Home
from com_dayoung_api.movie.api import Movie, Movies
from com_dayoung_api.review.api import Review, Reviews
from com_dayoung_api.user.api import User, Users, Auth, Access
from com_dayoung_api.actor.api import Actor, Actors

def initialize_routes(api):
    print("================ 2 route ====================")
    api.add_resource(Home, '/api')
    api.add_resource(Movie, '/Movie/<string:id>')
    api.add_resource(Movies, '/Movies')
    api.add_resource(Review, '/Review<string:id>')
    api.add_resource(Reviews, '/Reviews')
    api.add_resource(User, '/User<string:id>')
    api.add_resource(Users, '/Users')
    api.add_resource(Auth, '/api/auth')
    api.add_resource(Access, '/api/access')
    api.add_resource(Actor, '/Actor<string:id>')
    api.add_resource(Actors, '/Actors')
    
    
