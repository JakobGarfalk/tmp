from sqlalchemy.orm import query, backref
from sqlalchemy import text, func
from flask import session, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from BLOG import Kontroll, db

from BLOG.models import Comment, Bruker, UserPost, Dagbok


class Brain:  # henter brukernavn & id fra session obj, el. sletter fra session
    """Brain objektet inneholder brukernavn & ID og interagerer med session objektet"""

    sesVar = "minBruker"  # <--- nøkkelen som finnes i session (normalt et objekt i flask) kan defineres her
    sesVarID = "minBrukerID"  # <- value til denne key vil oppdateres ofte
    bruker = False  # <-verdiene vi faktisk trenger mange andre steder
    brukerID = (
        False  # <- pr nå bruker disse som mellomstasjon for values i session obj.
    )
    admin = False

    def __init__(self):  # må ha en instans for hver bruker
        print("_init_")
        self.brukernavn=Brain.bruker

    def load():
        """return brain.bruker hentet fra session"""
        if session.get(Brain.sesVar) != None and session.get(Brain.sesVarID) != None:
            setattr(Brain, "bruker", session.get(Brain.sesVar))
            setattr(Brain, "brukerID", session.get(Brain.sesVarID))
            # Brain.bruker=session.get(Brain.sesVar)
            # Brain.brukerID=session.get(Brain.sesVarID)
            print("from-session_", Brain.bruker, "-", Brain.brukerID)
            
        else:
            Brain.bruker = False
            Brain.brukerID = False
            print("_notInSession_")
        bruker=Brain.bruker
        return bruker
    def fog():  # Brain.fog() vil slette sessions variabler for minBruker; logout
        if session.get(Brain.sesVar) != None:
            print(Brain.bruker, "_is forgotten from-session_")
            session.pop(Brain.sesVar)
            session.pop(Brain.sesVarID)
            Brain.bruker = False
            Brain.brukerID = False
        bruker=Brain.bruker
        return bruker

def reqnavn_reqpass_sjekk__db(
    reqnavn, reqpass
):  # Bruker.brukernavn vil eksistere såfremt ikke db.query gir None
    """Funksjonen vil sjekke reqnavn og reqpass mot DB,
    sjekker db for: finnes brukernavn? stemmer request.form[psw1] med check_password_hash i Bruker.password_hash.
    Returnerer none eller Bruker.obj"""
    # reqnavn = request.form["uname1"]
    # reqpass = request.form["psw1"]
    # reqnavnStr = reqnavn.title()
    # finnDB1 = Bruker.query.filter(
    #     Bruker.brukernavn == reqnavnStr
    # ).first()  # , Bruker.passord==reqpass).first()
    # finnDB1 = Bruker.query.filter(
    #     func.lower(Bruker.brukernavn) == func.lower(reqnavn)
    # ).first()
    finnDB1 = (
        db.session.query(Bruker)
        .filter(func.lower(Bruker.brukernavn) == func.lower(reqnavn))
        .first()
    )

    if finnDB1 == None:
        flash("feil brukernavn!")
        print("f_sjekk_db=None")
    else:
        print(
            "psw chk=",
            check_password_hash(pwhash=finnDB1.password_hash, password=reqpass),
        )
        if check_password_hash(pwhash=finnDB1.password_hash, password=reqpass) == False:
            flash("Feil passord!")
            return None

        print(finnDB1.brukernavn, "<--forsøkes logges inn.")
        session[Brain.sesVar] = finnDB1.brukernavn  # gjelder for denne session
        session[Brain.sesVarID] = finnDB1.id
        print("ID:", session.get(Brain.sesVarID))
    return finnDB1


def hentBruker_db(reqnavn=None, reqID=None):
    """Oppgi reqnavn, ELLER reqID & få returnert Bruker.query.object"""
    if reqnavn == False or reqnavn == None and reqID==None:
        print("funk_hentBruker oppgitt none/false reqnavn..")
        return None   
    if reqnavn!=False or reqnavn!=None:
        finnDB1 = (db.session.query(Bruker)
        .filter(func.lower(Bruker.brukernavn) == func.lower(reqnavn))
        .first())
    elif reqID!=None:
        finnDB1 = (db.session.query(Bruker).filter(Bruker.id==reqID).first())

    return finnDB1


def opprett_nybruker(
    fname=None, lname=None, uname=None, email1=None, psw1=None, rett1=None
):
    """oppretter bruker, kan gis args: fname,lname,uname,email1,psw1,rett1
    - dersom ingen args oppgis brukes request.form["fname"], osv som default
    - return msg string"""

    if fname == None or uname == None or psw1 == None:
        fname = request.form["fname"]
        lname = request.form["lname"]
        uname = request.form["uname"]
        #uname1 = str(uname)
        email1 = request.form["email"]
        psw1 = request.form["psw1"]
        rett1 = "Standard"

    print("req.form=", fname, "& ", lname, " & ", uname, " & ", psw1)
    
    prevent_double = hentBruker_db(uname)
    #db.session.query(Bruker).filter(func.lower(Bruker.brukernavn) == func.lower(uname)).first()
    if prevent_double != None:
        msg = "Brukernavn er allerede i bruk!"
        return msg
    else:
        pswhash = generate_password_hash(psw1, salt_length=200)
        ny = Bruker(
            fornavn=fname,
            etternavn=lname,
            brukernavn=uname,
            email1=email1,
            rettighet=rett1,
            passord="passord saltes og hashes før lagring i databasen",
            password_hash=pswhash,
        )

        db.session.add(ny)
        db.session.commit()
        beskjedSTR = "bruker: " + ny.brukernavn + " legges til med ID:" + str(ny.id)
        # flash(beskjedSTR)
        msg = beskjedSTR
        print("Lagt til->", ny.fornavn, "-ID", ny.id)
        return msg