"""
func: bruker_fra_db, ny_bruker_db, (erstatter loginbruker.py)
les_comments, les_poster, send_melding
"""
from flask.globals import current_app
from BLOG import Kontroll, db

# from BLOG.custom_login import current_user
# current_user er none før context, så skal en bruke current_user her må en sette en def
from BLOG.models import Comment, Bruker, UserPost, Meldinger
from sqlalchemy import text, func, desc
from werkzeug.security import generate_password_hash, check_password_hash, gen_salt

""" 
## LITT OM QUERY OPS:
q=Bruker.query.filter(Bruker.id>0).count()
#--> gir en INT, i dette tilfellet antall brukere.
.filter(func.lower(Bruker.brukernavn))==    lowercase, husk import text, ->func, desc fra SQLalchemy
.order_by(UserPost.dato.desc()).paginate(side, poster pr side, False)
#--> gir pagination objekt, display som dikt.
#### .paginate(1,4,False) betyr; vi er på side 1, 4 poster pr side, errormsg=False - hvis True vil en tom liste gi 404 feil.
"""


def bruker_fra_db(reqnavn=None, reqID=None):
    """Oppgi reqnavn, ELLER reqID & få returnert Bruker.query.object"""

    if not reqnavn == False and not reqnavn == None:
        finnDB1 = (
            db.session.query(Bruker)
            .filter(func.lower(Bruker.brukernavn) == func.lower(reqnavn))
            .first()
        )
    if not reqID == None and reqnavn == None:
        _reqID = int(reqID)
        # finnDB1 = (db.session.query(Bruker).filter(Bruker.id==_reqID).first())
        db.session.query(Bruker).get(_reqID)
    return finnDB1


def ny_bruker_db(
    fornavn="Zoe",
    etternavn="Quinn",
    brukernavn="ZoeQu",
    email1="ZoeQ@local.ho",
    rettighet="Bruker",
    passord="python",
):
    """oppretter ny bruker, return msg string"""
    password_hash = generate_password_hash(passord, salt_length=200)

    prevent_double = bruker_fra_db(reqnavn=brukernavn)
    if prevent_double != None:
        msg = "Brukernavn er allerede i bruk!"
        return msg
    else:
        ny = Bruker(
            fornavn=fornavn,
            etternavn=etternavn,
            brukernavn=brukernavn,
            email1=email1,
            rettighet=rettighet,
            passord="passord saltes og hashes før lagring i databasen",
            password_hash=password_hash,
        )
        db.session.add(ny)
        db.session.commit()
        beskjedSTR = "bruker: " + ny.brukernavn + " legges til med ID:" + str(ny.id)
        # flash(beskjedSTR)
        msg = beskjedSTR
    return msg


def les_comments(limit=3, page=""):
    """default returns 3 comments
    PAGINATION objects må sendes som som c.items dersom de skal itereres"""
    config = current_app.config
    COMMENTS_PER_PAGE = config.get("COMMENTS_PER_PAGE", 1)
    POST_PER_PAGE = config.get("POST_PER_PAGE", 1)
    # COMMENTS_PER_PAGE=Kontroll.config['COMMENTS_PER_PAGE'] or 1
    if page == "":
        c = db.session.query(Comment).order_by(desc(Comment.id)).limit(limit)
    else:
        c = Comment.query.order_by(Comment.dato.desc()).paginate(
            page, COMMENTS_PER_PAGE, False
        )
    return c


def les_poster(limit=1, page=""):
    """HUSK AT PAGINATION OBJECTS OPPFØRER SEG LITT ANNERLEDES;
    dvs. istedenfor å sende poster, må en sende poster.items til templat for iterering.
    default returns 1 (siste) post"""
    config = current_app.config
    COMMENTS_PER_PAGE = config.get("COMMENTS_PER_PAGE", 1)  # get('X',defaultverdi)
    POST_PER_PAGE = config.get("POST_PER_PAGE", 1)          # hvis ikke key finnes settes 1
    # POST_PER_PAGE=Kontroll.config['POST_PER_PAGE'] or 1

    if not page == "":
        p1 = (
            db.session.query(UserPost)
            .order_by(UserPost.dato.desc())
            .paginate(page, POST_PER_PAGE, False)
        )
        # p1 = db.session.query(UserPost).order_by(desc(UserPost.id)).xxx()
    elif page == "alle":
        p1 = db.session.query(UserPost).order_by(desc(UserPost.id)).all()
    elif page == "":
        p1 = db.session.query(UserPost).order_by(desc(UserPost.id)).limit(limit)
    return p1


def send_melding(tittel, innhold, forfatter_id, send_til_id, lest="ikke lest"):
    """tittel, innhold, fra_bruker(id), til_bruker(id)"""
    m1 = Meldinger(
        tittel=tittel, innhold=innhold, forfatter_id=forfatter_id, send_til=send_til_id, lest=lest
    )
    ## i models.py har lest default verdi som "ikke lest", så den behøver ikke oppgis.
    ## men ettersom send_melding kan gjenbrukes i les_melding og sett lest="sett"
    db.session.add(m1)
    db.session.commit()
    return "fra={0}  til={1}".format(forfatter_id,send_til_id)

def ny_post_db(tittel, slug, forfatter_id, innhold="Det var en gang"):
    pny1 = UserPost(
        tittel=tittel, slug=slug, forfatter_id=forfatter_id, innhold=innhold
    )
    db.session.add(pny1)
    db.session.commit()
