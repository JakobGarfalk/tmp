from dotenv import load_dotenv  # egentlig ikke nødvendig, alt ligger nå i config.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager
from BLOG.custom_login import LoginManager
# from sqlalchemy import create_engine, MetaData
from flask_migrate import (
    Migrate,
)  # for å kunne endre (nesten automatisk) på databasen uten å slette den.
import config
import os

# ## - overføre til vanlig SQLalchemy? :--
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# ## --
# Kontroll=Flask(__name__)    # setter flask dir, kan bruke: app=Flask(__name__,instance_path='/path/to/instance/folder')
# husk at her kjøres Flask server, og de innstillinger som er satt er de en vil få se.

from logging.handlers import RotatingFileHandler
import logging

# ...

# if not Kontroll.debug:
#     # ...

#     if not os.path.exists('logs'):
#         os.mkdir('logs')
#     file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
#                                        backupCount=10)
#     file_handler.setFormatter(logging.Formatter(
#         '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)

#     app.logger.setLevel(logging.INFO)
#     app.logger.info('Microblog startup')
# --KONFIG FRA FIL:
# Kontroll.config.from_pyfile(config.py)

# -.ENV
# dirTilEnvFil='..'
load_dotenv(
    dotenv_path="BLOG/.env"
)  # env kan være fint når en ønsker verdiene satt i os.environ raskt, men...

envTilDikt = os.environ.get(
    "SJEKK_DETTE"
)  # Sjekker om .env fil har lastet til os.environ
SECRET_KEY = os.environ.get("SECRET_KEY")
print(envTilDikt)

env_vars = []  ## hvis det skal brukes er muligheten der
key_antall = os.environ.get("HENTE_ANT")
for antall in key_antall:
    key_value = os.environ.get(antall)
    env_vars.append(key_value)
print(env_vars)

# OSinfobrukerid=os.geteuid()
# Return the current process’s effective user id.
# Availability: Unix. i windows error: os has no attribute id.

# OSinfobrukergruppe=os.getgid()
# Return the real group id of the current process.
# Availability: Unix.


# -------------------TIL CONFIG FIL:
# konfigdir = os.path.abspath(os.path.dirname(__file__))

# -----------------
# from BLOG.konfig.config import Config

Kontroll = Flask(
    __name__
)  # liten hensikt å konfigurere Flask før .env er lastet, men da gjelder .env, ikke launch.json
login_man = LoginManager(Kontroll)
login_man.login_view="login_bruker_view"

#login_man.init_app
# ---IMPORT I MODULER:

# ...

# Kontroll.config.from_pyfile("../config.py")
Kontroll.config.from_object(config.Config)
Kontroll.config["SECRET_KEY"] = SECRET_KEY
# Kontroll.config['SECRET_KEY']=os.environ.get('SECRET_KEY') # verdier fra .env må settes slik, de ligger i os.environ (os.environ = dict)

db = SQLAlchemy(Kontroll)  # db
migrate = Migrate(Kontroll, db)
# --------------------

# engine2 = create_engine(
#     "sqlite:///sqlite3.db", encoding="UTF-8", echo=True
# )  # skal da bruke db def i config
# db2 = engine2.connect()
# metadata2 = MetaData(bind=db2)

# 2 binds til samme fil ser ut til å fungere, men for å unngå data-korrupsjon må en være nøye med threading; åpne&lukke session.
#def init_db2(FILENAME="DBfil2.DB")
initDB2=False
if initDB2==True:
    engine = create_engine("sqlite:///blog2.db", encoding="UTF-8", echo=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# db_session2 = sessionmaker(bind=engine2)
    Base = declarative_base(bind=engine)
    Base.query = db_session.query_property()

### LOGGER:
LOG_AKTIV=True
if LOG_AKTIV==True:
    # ...

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/blog.log', maxBytes=10240,backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    ### logging.INFO ; DEBUG, INFO, WARNING, ERROR, CRITICAL =grad av hvor mye som logges
    Kontroll.logger.addHandler(file_handler)
    Kontroll.logger.setLevel(logging.INFO)
    Kontroll.logger.info('BLOG startup')

#config=current_app.config
RECAPTCHA_PUBLIC_KEY=Kontroll.config['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY=Kontroll.config['RECAPTCHA_PRIVATE_KEY']
# ----------# Nå er config satt, og resten av programmet kan kobles sammen:


#from BLOG.models import Bruker,Comment
from BLOG import views
#from BLOG import forms
