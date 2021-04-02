from BLOG.custom_login.config import LOGIN_MESSAGE, LOGIN_MESSAGE_CATEGORY, REFRESH_MESSAGE, REFRESH_MESSAGE_CATEGORY
import os

konfigdir = os.path.abspath(os.path.dirname(__file__))  # hvor vi legger DB


class Config:
    FLASK_APP = "/BLOG/"  # oppgitt i launch.json, oppgitt i .env
    FLASK_ENV = "development"  # oppgitt i launh.json  oppgitt i .env
    # SECRET_KEY = 'gjett3ganger3destroythemall'   #oppgitt i .env
    # DEBUG = True
    TESTING = True      # noe error handling som ellers ikke vises vil nå vises om 'True'
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(konfigdir, "blog.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_NAME = "CookieBlog"
    SQLALCHEMY_POOL_RECYCLE = 299  # etter 299 sek uten aktivitet brytes connect
    SQLALCHEMY_ECHO = True  # Alt til-fra db vises i konsoll for debug formål
    STATIC_FOLDER = "static"  # default=static
    TEMPLATES_FOLDER = "templates"  # default=templates
    POST_PER_PAGE = 1
    COMMENTS_PER_PAGE = 2
    RECAPTCHA_PUBLIC_KEY="micromanagingtesting1223"
    RECAPTCHA_PRIVATE_KEY="testing123micromanagingexploringdoringchoring"
    ### login man:
    LOGIN_MESSAGE = "innlogging kreves."
    LOGIN_MESSAGE_CATEGORY = "messages"
    REFRESH_MESSAGE = "Re-autorisering kreves."
    REFRESH_MESSAGE_CATEGORY = "messages"
    REFRESH_VIEW = "index"  # her eller i _init_?

    print("Lastet konfig.")


# Kontroll.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'

# FLASK_APP='/BLOG/'  # oppgitt i launch.json, oppgitt i .env
# #FLASK_ENV='development' # oppgitt i launh.json  oppgitt i .env
# SECRET_KEY = 'gjett3ganger3ganger3'   #oppgitt i .env
# #DEBUG = True
# #TESTING = True      # noe error handling som ellers ikke vises vil nå vises om 'True'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(konfigdir, 'blog.db')
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SESSION_COOKIE_NAME = 'CookieBlog'
# SQLALCHEMY_POOL_RECYCLE = 299 # etter 299 sek uten aktivitet brytes connect
# SQLALCHEMY_ECHO = True        # Alt til-fra db vises i konsoll for debug formål
# STATIC_FOLDER = 'static'       # default=static
# TEMPLATES_FOLDER = 'templates'  # default=templates
