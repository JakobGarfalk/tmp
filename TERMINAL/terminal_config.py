

class Config():
    SQL_FILE = "terminal.db"
    FLASK_ENV = "development"  # oppgitt i launh.json  oppgitt i .env
    LOG_AKTIV=True ## error logger
    SECRET_KEY = 'pbkdf2:sha256:150000$nb5qgXSe$1555dcc3976e10663dfb6e444329f589a34aef7fd1e21f2c26a8efc5c98897f6'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQL_FILE
    SQLALCHEMY_TRACK_MODIFICATIONS = False ########### <------ SENKER YTELSE IF TRUE
    # DEBUG = True
    TESTING = False      # noe error handling som ellers ikke vises vil nå vises om 'True'
    
    SESSION_COOKIE_NAME = "Terminal"
    SQLALCHEMY_POOL_RECYCLE = 299  # etter 299 sek uten aktivitet brytes connect
    SQLALCHEMY_ECHO = True  # Alt til-fra db vises i konsoll for debug formål
    STATIC_FOLDER = "static"  # default=static
    #TEMPLATES_FOLDER = "templates"  # default=templates
    POST_PER_PAGE = 2
    COMMENTS_PER_PAGE = 3
    RECAPTCHA_PUBLIC_KEY="micromanagingtesting1223"
    RECAPTCHA_PRIVATE_KEY="testing123micromanagingexploringdoringchoring"
    ### login man: flyttes til __init; dette er ikke verdier som egentlig skal endres på.
    LOGIN_MESSAGE = "innlogging kreves."
    LOGIN_MESSAGE_CATEGORY = "messages"
    REFRESH_MESSAGE = "Re-autorisering kreves."
    REFRESH_MESSAGE_CATEGORY = "messages"
    REFRESH_VIEW = "main.index"  # her eller i _init_?

    print("TERMINAL_CONFIG EOF.READ") # bekfreft når config eof er nådd.

# class ProdConfig():
#     FLASK_ENV="production"
#     DEBUG=False
#     TESTING=False
#     SESSION_COOKIE_NAME="Term_pro4"
#     print ("ProdConfig EOF")
