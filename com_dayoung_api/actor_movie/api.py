from typing import List
from flask_restful import Resource, reqparse
from com_dayoung_api.actor_movie.dao import ActorMovieDao
from com_dayoung_api.actor_movie.dto import ActorMovieDto

class ActorMovie(Resource):
    def __init__(self):
        parser = reqparse.RequestParser() # only allow price changes, no name changes allowed
        parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')
        parser.add_argument('store_id', type=int, required=True, help='Must enter the store id')
        self.dao = ActorMovieDao

    def get(self, name):
        item = self.dao.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

class Actors_movie(Resource):
    def get(self):
        ...