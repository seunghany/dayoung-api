import logging
from flask import Blueprint
from flask_restful import Api
from com_dayoung_api.user.api import User

user = Blueprint('user', __name__, url_prefix='/api/user')
users = Blueprint('users', __name__, url_prefix='/api/users')
auth = Blueprint('auth', __name__, url_prefix='/api/auth')
access = Blueprint('access', __name__, url_prefix='/api/access')
api = Api(user)
api = Api(users)
api = Api(auth)
print("==============3 user/init==================")
api = Api(access)
print("================4  user/init.api================")

@user.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during user request. %s' % str(e))
    return 'An internal error occurred.', 500