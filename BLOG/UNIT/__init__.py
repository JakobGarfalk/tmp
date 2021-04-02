#from BLOG import Kontroll, db
#from BLOG.models import Bruker, UserPost
from flask import Flask
from BLOG.custom_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
#from BLOG.UNIT import unit_testing
from . import unit_testing
from .config import (SQLALCHEMY_DATABASE_TEST,SECRET_KEY)

SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_TEST
app_test=Flask(__name__)
db = SQLAlchemy(app_test)

def __go():

    unit_testing.py

__go()

