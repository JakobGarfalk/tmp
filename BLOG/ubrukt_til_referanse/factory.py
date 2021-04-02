#from sqlalchemy.orm import query
from BLOG import Kontroll, db

#from flask_sqlalchemy import SQLAlchemy # Flask Sqlalchemy lager automatisk sessionmaker,session, create_engine, mm.
#from flask_migrate import Migrate
from flask import request, render_template, redirect
from flask import flash, url_for, make_response, session, escape
from flask import jsonify   # sende info i json format
from datetime import datetime
from BLOG.models import Comment, Bruker, UserPost, Dagbok, BrukerStat
#import os


#session={'minBruker':"Wotan",'minBrukerID':200}

class Brain():  # henter brukernavn & id fra session obj, el. sletter fra session
    sesVar='minBruker' # <--- nøkkelen som finnes i session (normalt et objekt i flask) kan defineres her
    sesVarID='minBrukerID' # <- value til denne key vil oppdateres ofte
    bruker=False # <-verdiene vi faktisk trenger mange andre steder
    brukerID=False # <- pr nå bruker disse som mellomstasjon for values i session obj.
    def __init__(self):        
        print ("init_")
        
        if session.get(Brain.sesVar)!=None and session.get(Brain.sesVarID)!=None:
            setattr(Brain, 'bruker', session.get(Brain.sesVar))
            setattr(Brain, 'brukerID', session.get(Brain.sesVar))
            #Brain.bruker=session.get(Brain.sesVar)
            #Brain.brukerID=session.get(Brain.sesVarID)
            print ("from-session_",Brain.bruker)
        else:
            Brain.bruker=False
            Brain.brukerID=False
            print ("notInSession_")
    
    def fog():  # Brain.fog() vil slette sessions variabler for minBruker; logout
        if session.get(Brain.sesVar)!=None:
            print (Brain.bruker,"_is forgotten from-session_")
            session.pop(Brain.sesVar)
            session.pop(Brain.sesVarID)
            Brain.bruker=False
            Brain.brukerID=False

# class Brain():  # henter brukernavn & id fra sessions
#     bruker=False
#     brukerID=False
#     def __init__(self):        
#         print ("init_")
#         Brain.bruker , Brain.BrukerID= sjekkSession()
#         if not session.get('minBruker')==None or not session.get('minBrukerID')==None:
#             Brain.bruker=session.get('minBruker')
#             Brain.brukerID=session.get('minBrukerID')
#             print ("from-session_",Brain.bruker)
#         else:
#             Brain.bruker=False
#             Brain.brukerID=False
#             print ("notInSession_")
    
#     def fog():  # Brain.fog() vil slette sessions variabler for minBruker; logout
#         if session.get('minBruker')!=None:
#             print (Brain.bruker,"_is forgotten from-session_")
#             session.pop('minBruker')
#             session.pop('minBrukerID')
#     def load():  #Brain.load - returnerer DB verdier for bruker
#         id=None
#         if not Brain.bruker==False or Brain.brukerID==False:
#             hentBruker=Bruker.query.filter(Bruker.brukernavn==Brain.bruker, Bruker.id==Brain.brukerID).first()
#             id=hentBruker.id
#         return id
#     def sjekkSession():
#         if not session.get('minBruker')==None or not session.get('minBrukerID')==None:
#             return session.get('minBruker'),session.get('minBrukerID')
#         else:
#             return False,False

class Laster(): # problemstillinger er at db.query gir objekter hvis noe finnes.
    def inn():  # Bruker.brukernavn vil eksistere såfremt ikke db.query gir None
        reqnavn=request.form["uname1"]
        reqpass=request.form["psw1"]
        reqnavnStr=reqnavn.title()
        finnDB1=Bruker.query.filter(Bruker.brukernavn==reqnavnStr, Bruker.passord==reqpass).first()

hentBruker=Brain.bruker