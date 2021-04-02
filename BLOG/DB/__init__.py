from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

import os

print("1:", __file__)
print("2:", os.path.join(os.path.dirname(__file__), ".."))
print("3:", os.path.dirname(os.path.realpath(__file__)))
print("4:", os.path.abspath(os.path.dirname(__file__)))
konfigdir = os.path.abspath(os.path.dirname(__file__))
# uten konfigdir havner fil i root, som er korrekt pr nå.

engine2 = create_engine(
    "sqlite:///admin.db",
    encoding="UTF-8",
    echo=True,
)
db_session2 = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine2)
)
# db_session2 = sessionmaker(bind=engine2)
Base2 = declarative_base(bind=engine2)
Base2.query = db_session2.query_property()

from BLOG.DB import models