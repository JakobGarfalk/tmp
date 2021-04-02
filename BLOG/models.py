"""Models for: Comment, Bruker, UserPost, Meldinger, 
"""
from BLOG import Kontroll, db
from BLOG import login_man
# det er forholdsvis enkelt å konvertere til SQLalchemy,
# men Flask-SQLAlchemy er bedre for å unngå thread error,
# evt kjør SQLAlchemy modeller der du er nøye med session.close etter hver query.
# from BLOG import engine, Base, db_session

from flask_sqlalchemy import SQLAlchemy
#from flask_login import UserMixin
from BLOG.custom_login import UserMixin, AnonymousUserMixin
from flask_migrate import Migrate, current
# from flask import request, render_template, url_for, redirect, flash
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from sqlalchemy.orm import relationship, backref

# @login.user_loader
# def load_user(id):
#     return Bruker.query.get(int(id))
# ---MODELS: -------HUSK NÅR DU KJØRER FLASK MIGRATE; gjør det fra ny powershell terminal, ellers ses kanskje ikke endringer!
# f=Comment.query.all() returnerer en liste som kan loopes med for-loop,
# det er altså en liste med objekter i. liste: objekt1, objekt2.
# tilgang til objektene blir som ellers med for x in listen: x.objattributt1 x.objattr2 osv.
# f.Comment.query.all()
# for k in f: (ID 1,2,3... ID1=objekt1.innhold osv)
#   print (k.innhold)
#   print (k.dato)
# f=Bruker.query.filter(Bruker.id==2).first() returnerer et objekt; f.brukernavn osv
# print (f.brukernavn)  <--- går fordi det kun er et objekt med .first()
class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    innhold = db.Column(db.String(4096))
    forfatter = db.Column(db.String(40), default="anonym")
    dato = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        s="ID={} forfatter={} dato={} \n innhold={}" #.format( {self.id}, {self.forfatter}, {self.dato}, {self.innhold})
        return s.format({self.id}, {self.forfatter}, {self.dato}, {self.innhold} ) #{self.id,self.forfatter, self.dato, self.innhold})
### -- many:to:many tables:
# venner = db.Table('venner',
#     db.Column('bruker_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('venn_id', db.Integer, db.ForeignKey('users.id'))
# )


# melding.id = EN, melding_til = MANY
# melding_kart = db.Table('melding_kart',
# db.Column('melding_id',db.Integer,db.ForeignKey('meldinger.id')),
# db.Column('melding_fra',db.Integer,db.ForeignKey('users.id')),
# db.Column('melding_til',db.Integer,db.ForeignKey('users.id'))
# )
# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

#     def __repr__(self):
#         return '<Message {}>'.format(self.body)
# class User(db.Model):
#     # ...
#     messages_sent = db.relationship('Message',
#                                     foreign_keys='Message.sender_id',
#                                     backref='author', lazy='dynamic')
#     messages_received = db.relationship('Message',
#                                         foreign_keys='Message.recipient_id',
#                                         backref='recipient', lazy='dynamic')
#     last_message_read_time = db.Column(db.DateTime)

#     # ...

#     def new_messages(self):
#         last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
#         return Message.query.filter_by(recipient=self).filter(
#             Message.timestamp > last_read_time).count()


@login_man.user_loader
def load_user(id):
    # .get(int(id)) id primary keys i SQL DB, er INTEGER, mens login_man bruker STR.
    # derfor må en konvertere TIL INT når en henter fra load_user
    return Bruker.query.get(int(id))


class AnonymBruker(AnonymousUserMixin):
    id=0
    fornavn=""
    etternavn=""
    brukernavn=False
login_man.anonymous_user = AnonymBruker

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id'),primary_key=True, autoincrement=False),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'),primary_key=True, autoincrement=False)
)

class Bruker(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    dato = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    fornavn = db.Column(db.String(40))
    etternavn = db.Column(db.String(40))
    brukernavn = db.Column(
        db.String(40), index=True, unique=True
    )  # unique gir feilmelding hvis forsøkes brutt
    rettighet = db.Column(db.String(40), default="Standard")
    passord = db.Column(db.String(255))
    logindato = db.Column(db.DateTime(), default=datetime.utcnow)
    email1 = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(255))
    ### RELATIONSHIPS ####
    ### Merk, når en har flere FK som peker mellom samme tables, brukes foreign_keys='Class.var_til_FK'
    ### lazy='dynamic' betyr at et nytt query object dannes,
    ### dette brukes for å begrense mengden resultat data.
    #endre vennskap til venner_med, backref=venner henviser til de som er venner med meg
    # vennskap = db.relationship('Bruker', secondary=venner, primaryjoin=(venner.c.bruker_id == id), 
    # secondaryjoin=(venner.c.venn_id==id),
    # backref=db.backref('venner',lazy='dynamic'),lazy='dynamic')
    melding_fra_bruker = db.relationship('Meldinger',foreign_keys='Meldinger.forfatter_id',backref='melding_fra', lazy='dynamic')
    melding_til_bruker = db.relationship('Meldinger',foreign_keys='Meldinger.send_til',backref='melding_til', lazy='dynamic')
    poster_fra_bruker = db.relationship('UserPost', foreign_keys='UserPost.forfatter_id', backref='poster_fra')
    comments_fra_bruker =db.relationship('PostComments', foreign_keys='PostComments.forfatter_id', backref='comments_fra')
    annonser_fra_bruker = db.relationship('Annonser', foreign_keys='Annonser.forfatter_id', backref='annonser_fra',lazy='dynamic')

    followed = db.relationship(
        'Bruker', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')


    def __repr__(self):
        return (
            f"<ID: {self.id}, brukernavn={self.brukernavn},logindato= {self.logindato}>") #, venner= {self.vennskap}"
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        # return 
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def get_id(self):
        return str(self.id)
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
    def is_following(self, user): #UserPost.query.join(followers, (followers.c.followed_id == UserPost.user_id))
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    


    def only_followed_posts(self):
        return UserPost.query.join(
            followers, (followers.c.followed_id == UserPost.forfatter_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    UserPost.dato.desc())
    def followed_posts(self):
        followed = UserPost.query.join(
            followers, (followers.c.followed_id == UserPost.forfatter_id)).filter(
                followers.c.follower_id == self.id)
        own = UserPost.query.filter_by(forfatter_id=self.id)
        return followed.union(own).order_by(UserPost.dato.desc())

    def obj_til_dict(self):
        """hent query objekt, få dikt i var d = Bruker.objtildikt(queryobj)
        ex. finnDB1 = Bruker.query.filter(Bruker.brukernavn == "Jdg").first()
        d = Bruker.objtildikt(finnDB1)"""
        dict_var = {
            "id": self.id,
            "dato": self.dato,
            "fornavn": self.fornavn,
            "etternavn": self.etternavn,
            "brukernavn": self.brukernavn,
            "email1": self.email1,
            "passord": self.passord,
            "password_hash": self.password_hash,
            "logindato": self.logindato,
        }
        return dict_var


class UserPost(db.Model):
    """ {% for post in poster %}
        <h2>{{ post.tittel }}</h2>
        <small>forfatter: {{ post.poster_fra.fornavn }} {{ post.poster_fra.etternavn }} </small>"""
    __tablename__ = "poster"
    id = db.Column(db.Integer(), primary_key=True)
    tittel = db.Column(db.String(255), nullable=False, index=True)
    slug = db.Column(db.String(255), nullable=False)
    innhold = db.Column(db.Text(), nullable=False)
    dato = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    oppdatert = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    ### FOREIGN KEYS:
    forfatter_id= db.Column(db.Integer, db.ForeignKey("users.id"))
    #### RELATIONSHIPS: ####
    #forfatter=db.relationship("Bruker", backref="poster") #flyttet til Bruker
    comment_rel=db.relationship('PostComments', foreign_keys='PostComments.post_id', backref='comments_on_post',lazy='dynamic')
    def __repr__(self):
        return (f"ID: {self.id} {self.tittel} {self.forfatter_id}")
#siste=UserPost.query.filter(UserPost.forfatter_id==current_user.id).order_by(UserPost.dato.desc())
class PostComments(db.Model):
    """post_id=FK poster.id"""
    __tablename__="postcomments"
    id = db.Column(db.Integer(), primary_key=True)
    tittel = db.Column(db.String(255), nullable=False)
    innhold = db.Column(db.Text(), nullable=False)
    ### FOREIGN KEYS:
    post_id= db.Column(db.Integer, db.ForeignKey("poster.id")) #UserPost backref=comments
    forfatter_id=db.Column(db.Integer, db.ForeignKey("users.id")) #Bruker backref=comments

    


class Dagbok(db.Model):
    __tablename__ = "dagbok"

    id = db.Column(db.Integer, primary_key=True)
    dato = db.Column(db.DateTime, default=datetime.now, index=True)
    oppdatert = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    # tittel = db.Column(db.String(255), nullable=False)
    # # kapittel = db.column(db.String(40))
    # innhold = db.Column(db.String(4096))

### eks på many:to:many via table:   sett opp kart table via db.Tabl : kart = 
# association_table = Table('association', Base.metadata,
#     Column('left_id', Integer, ForeignKey('left.id')),
#     Column('right_id', Integer, ForeignKey('right.id'))
# )

# class Parent(Base):
#     __tablename__ = 'left'
#     id = Column(Integer, primary_key=True)
#     children = relationship("Child",
#                     secondary=association_table,
#                     backref="parents")

# class Child(Base):
#     __tablename__ = 'right'
#     id = Column(Integer, primary_key=True)

class Annonser(db.Model):
    __tablename__ = "annonser"
    id = db.Column(db.Integer, primary_key=True)
    # id=db.Column(db.Integer,db.Foreignkey("users.id") primary_key=True)
    tittel = db.Column(db.String(255), nullable=False)
    innhold = db.Column(db.String(4096))
    kategori = db.Column(db.String(255), nullable=False)
    forfatter_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #annonser = db.relationship('Bruker', foreign_keys='forfatter.id', backref='mine_annonser',lazy='dynamic')
# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

#     def __repr__(self):
#         return '<Message {}>'.format(self.body)
class Meldinger(db.Model):
    __tablename__ = "meldinger"
    id = db.Column(db.Integer, primary_key=True)
    dato = db.Column(db.DateTime, default=datetime.now, index=True)
    tittel = db.Column(db.String(255))
    innhold = db.Column(db.String(1024))
    forfatter_id= db.Column(db.Integer, db.ForeignKey("users.id"))
    send_til=db.Column(db.Integer, db.ForeignKey("users.id"))
    lest=db.Column(db.String(10),default="ikke lest")

def run_local_models():
    db.create_all()


# # lage tables med vanlig declarative_base i sqlalchemy:
# Base.metadata.create_all(bind=engine)
if __name__=="__main__":
    run_local_models()