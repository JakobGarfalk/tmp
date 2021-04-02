# -------manuell mapping som tilsvarer declarative_base
print("LA MEG VITE OM DENNE KJØRES!")
x = input("Trykk enter, eller ctrl-C om du ikke er meg! ('q' vil også avslutte)")
if x == "q" or x == "e" or str(x.lower) == "quit" or str(x.lower) == "exit":
    exit()

#### manuell mapping som tilsvarer declarative_base:
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

engine2 = create_engine("sqlite:////tmp/test.db", convert_unicode=True)
metadata2 = MetaData()  # alternativ måte uten declarative_base
db_session2 = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine2)
)
# hvis en utelukkende skal bruke SQL språk trenger en bare engine oppsett:
# engine=create_engine('sqlite:///temp.db')
# metadata=MetaData(bind=engine)
# ---> from sqlalchemy import Table
#      users = Table('users', metadata, autoload=True)
# ---> con=engine.connect() \   con.execute(users.insert)

#### modell oppsett
### normalt egen fil:
from sqlalchemy import Table, String, Column, Integer, DateTime  # , Text,Boolean
from datetime import datetime
from sqlalchemy.orm import mapper

# bruker metadata slik:
# metadata2.create_all(bind=engine2) #dette kommer ETTER model mapping

# from BLOG.DB import meta2, db_session2


class Comment2m(object):
    query = db_session2.query_property()

    def __init__(self, innhold=None, forfatter=None):
        self.innhold = innhold
        self.forfatter = forfatter

    def __repr__(self):
        return "manuell table:kommentarer, innhold=%r" % (self.innhold)


kommentarer = Table(
    "kommentarer",
    metadata2,
    Column("id", Integer(), primary_key=True),
    Column("innhold", String(4096)),
    Column("forfatter", String(40)),
    Column("dato", DateTime, default=datetime.now),
)

mapper(Comment2m, kommentarer)  # manuell mapping av objekt til sql table


# metadata2.create_all(engine2)


db_session2.remove()  # lukker session
