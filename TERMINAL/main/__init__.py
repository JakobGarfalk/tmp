from flask import Blueprint

bp = Blueprint(name="main",import_name=__name__)
print ("loading:",__name__)
from TERMINAL.main import views