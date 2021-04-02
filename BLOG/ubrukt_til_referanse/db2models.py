# from sqlalchemy import create_engine,MetaData,Table,Column,Integer,
from datetime import datetime

# from BLOG import engine2


# from sqlalchemy import MetaData # declarative_base hånderer MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from sqlalchemy import Table, String, Column, Text, DateTime, Boolean, Integer

# scoped_session gjør at en slipper åpne session via g object i flask,
# og deretter with minapp.app_context

# def init_db2():
engine2 = create_engine("sqlite:///sqlite3.db", encoding="UTF-8", echo=True)
db_session2 = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine2)
)
# db_session2 = sessionmaker(bind=engine2)
Base2 = declarative_base(bind=engine2)
Base2.query = db_session2.query_property()

# start_db2=init_db2()

# -------manuell mapping som tilsvarer declarative_base
# from sqlalchemy import create_engine, MetaData
# from sqlalchemy.orm import scoped_session, sessionmaker

# engine2 = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
# metadata2 = MetaData()
# db_session2 = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine2))
# bruker metadata slik:
# metadata2.create_all(bind=engine2) #dette kommer ETTER model mapping
# meta2 = MetaData(bind=engine2) # alternativ måte uten declarative_base
# Comment2 = Table(
#     "kommentarer",
#     meta2,
#     Column("id", Integer(), primary_key=True),
#     Column("innhold", String(4096)),
#     Column("forfatter", String(40)),
#     Column("dato", DateTime, default=datetime.now),
# )
# meta2.create_all(engine2)


class Comment2(Base2):

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    innhold = Column(String(4096))
    forfatter = Column(String(40), default="anonym")
    dato = Column(DateTime, default=datetime.now)


Base2.metadata.create_all(bind=engine2)

c = Comment2(innhold="Er du helt fjern eller?")
db_session2.add(c)
db_session2.commit()

# lukke sessions, legg i @min-app.teardown
# @app.teardown_appcontext
# def shutdown_session(exception=None):
query_objekt1 = Comment2.query.all()
for x in query_objekt1:
    print(query_objekt1)

# db_session2.remove()
# db_session2.query
