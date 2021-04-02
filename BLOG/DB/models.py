from BLOG.DB import engine2, Base2, db_session2

from datetime import datetime
from sqlalchemy import Table, String, Column, Text, DateTime, Boolean, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Comment2(Base2):

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    innhold = Column(String(4096))
    forfatter = Column(String(40), default="anonym")
    dato = Column(DateTime, default=datetime.now)


class Brukere(Base2):
    __tablename__ = "brukere"
    id = Column(Integer, primary_key=True)
    dato = Column(DateTime, default=datetime.now)
    fornavn = Column(String(30))
    etternavn = Column(String(30))
    brukernavn = Column(String(40), index=True, unique=True)
    rettighet = Column(String(20))
    passord = Column(String(255))
    postet = relationship("Poster", backref="brukere", lazy="dynamic")
    logindato = Column(DateTime(), default=datetime.utcnow)
    email1 = Column(String(120), index=True, unique=True)
    password_hash = Column(String(255))


class Poster(Base2):
    __tablename__ = "poster"
    id = Column(Integer(), primary_key=True)
    tittel = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    innhold = Column(Text(), nullable=False)
    dato = Column(DateTime(), default=datetime.utcnow)
    oppdatert = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    postetAv = Column(Integer, ForeignKey("brukere.id"))


Base2.metadata.create_all(bind=engine2)

query_objekt1 = Comment2.query.all()
db_session2.remove()