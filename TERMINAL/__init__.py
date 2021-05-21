from flask import Flask
print (__name__)
from TERMINAL.terminal_config import Config

loaded="start"
print (loaded)
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print("attempt import main:")
    from TERMINAL.main import bp as main_bp
    print("attempt register main_bp")
    app.register_blueprint(main_bp)

    return app
