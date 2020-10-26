import logging
from flask import Blueprint
from flask_restful import Api
from com_dayoung_api.actor.api import Actor

actor = Blueprint('actor', __name__, url_prefix='/api/actor')
actors = Blueprint('actors', __name__, url_prefix='/api/actors')
auth = Blueprint('auth', __name__, url_prefix='/api/auth')
access = Blueprint('access', __name__, url_prefix='/api/access')
print( "actor :", actor, "actors:", actors,"auth :", auth, "access :", access)
api = Api(actor)
api = Api(actors)
api = Api(auth)
print("==============3 actor/init==================")
api = Api(access)
print("================4  actor/init.api================")

@actor.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during actor request. %s' % str(e))
    return 'An internal error occurred.', 500