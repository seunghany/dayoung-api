

# Database 만들기
from flask import Flask
# 파일: /app.py => main.py
url = "url"
app = Flask(__name__)                                       # 1
app.config['SECRET_KEY'] = 'this is secret'                 # 2 꼭 필요하진 않는듯 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # 3
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        # 4
db = SQLAlchemy(app)                                        # 5 

# 난 이렇게 함
app = Flask(__name__)                                       # 1
# 2. 꼭 없어도 될듯                                          # 2
app.config['SQLALCHEMY_DATABASE_URI'] = url                 # 3
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        # 4
db.init_app(app)                                            # 5

# 5번이 다른 이유
# There are two usage modes which work very similarly. 
# One is binding the instance to a very specific Flask application:

app = Flask(__name__)
db = SQLAlchemy(app)
# The second possibility is to create the object once and configure the application later to support it:

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app
# The difference between the two is that in the first case methods like create_all()
# and drop_all() will work all the time but in the second case a flask.Flask.app_context() has to exist.

db.init_app(app) # init_app(app)
# This callback can be used to initialize an application for the use with this database setup.
#  Never use a database in the context of an application not initialized that way or connections will leak.



from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SomeClass(Base):
    __tablename__ = 'some_table'
    id = Column(Integer, primary_key=True)
    name =  Column(String(50))

# Above, the declarative_base() callable returns a new base class from which all mapped classes should inherit.
# When the class definition is completed, a new Table and mapper() will have been generated.

# access the mapped Table
SomeClass.__table__

# access the Mapper
SomeClass.__mapper__