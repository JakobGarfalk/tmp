##### IKKE I BRUK. TEST FIL
from sqlalchemy.orm import query, backref
from BLOG import Kontroll, db
from BLOG.models import Comment, Bruker, UserPost, Dagbok


def sendemails(finnDB):
    emailsubject = "DB EMNE"
    emailtxt = "Dummydata"
    # with open("send.txt","r",encoding="UTF-8") as emaildata:
    #     emailsubject=emaildata.readline()
    #     emailtxt=emaildata.read()
    #     emaildata.close()
    return "Trenger server og mail extension"


def bruker_tiltxt(finnDB):
    with open("bruker.txt", "a", encoding="UTF-8") as fil:
        fil.write(finnDB.id)
        fil.write(finnDB.dato)
        fil.write(finnDB.fornavn)
        fil.write(finnDB.etternavn)
        fil.write(finnDB.brukernavn)
        fil.write(finnDB.password_hash)
        fil.write(finnDB.email1)
        fil.write(finnDB.logindato)
        fil.close()

    # setlogindato = Bruker.query.filter_by(id=login_db.id).update(
    #             dict(logindato="onupdate")
    #         )
    #         # login_
