from werkzeug.security import generate_password_hash
from BLOG import Kontroll, db

# from BLOG.DB import engine2, Base2, db_session2

from BLOG.models import Comment, Bruker, UserPost, Dagbok, Meldinger

# from BLOG.DB.models import Comment2, Brukere, Poster
from sqlalchemy.orm import query

# from sqlalchemy.orm import relationship, backref
from sqlalchemy import text, func

from BLOG.db_func import les_poster, ny_bruker_db, ny_post_db

# def auto_ny_post(ant=1):
#     with open("dummydata.txt","r",encoding="UTF-8") as f:
#         tittel=f.readline()
#         innhold=
import pickle

SAVE_FILENAME = "dummydata"


class AutoPost(object):
    def __init__(self, id, tittel, slug, innhold, forfatter_id):
        self.id = id
        self.tittel = tittel
        self.slug = slug
        self.innhold = innhold
        self.forfatter_id = forfatter_id

    def save(self):
        # with open(SAVE_FILENAME, "w", encoding="UTF-8") as filobj:
        with open(SAVE_FILENAME, "wb") as filobj:
            # filobj.write(str(self.people))
            pickle.dump(self, filobj)
        filobj.close()

    def auto_ny_post_db(
        self,
    ):  # tittel, slug, forfatter_id, innhold="Det var en gang"):
        pny1 = UserPost(
            tittel=self.tittel,
            slug=self.slug,
            forfatter_id=self.forfatter_id,
            innhold=self.innhold,
        )
        db.session.add(pny1)
        db.session.commit()

    def post_hent_til_auto(self, id):
        p1 = UserPost.query.get(id)
        self.id = (p1.id,)
        self.tittel = (p1.tittel,)
        self.slug = (p1.slug,)
        self.innhold = (p1.innhold,)
        self.forfatter_id = p1.forfatter_id


# p1=AutoPost(tittel="Et Eventyr",slug="Skjønner den",innhold="Så har jeg levert også",forfatter=2)
# p1.save()


class Loader(object):
    def __init__(self):
        self.post = self.load()

    def load(self):
        SAVE_FILENAME = "dummydata"
        with open(SAVE_FILENAME, "rb") as filobj:
            post = pickle.load(filobj)
        filobj.close()
        return post


# p1=AutoPost(tittel="Et Eventyr",slug="Skjønner den",innhold="Så har jeg levert også",forfatter=2)
# p1.save()
# p1=Loader()
# def post_henting(id):
#     p1=UserPost.query.get(id)
#     auto1=AutoPost(id=p1.id,tittel=p1.tittel,slug=p1.slug,innhold=p1.innhold,forfatter_id=p1.forfatter_id)
#     return p

# p1=UserPost.query.get(1)
# auto=AutoPost(id=p1.id,tittel=p1.tittel,slug=p1.slug,innhold=p1.innhold,forfatter_id=p1.forfatter_id)
# auto.save()
# print(auto.post)
# print(auto.post.tittel)
# a=AutoPost()
# a.post_hent_til_auto(2)
# a.auto_ny_post_db()
from random import choice
from datetime import datetime

antall = "123456789"
tid = str(datetime.utcnow())
tid2 = tid[-4]
# fornavn1=["Tor","Knut","Ariel","Marie","Oluf","Gustav","Adolf","Erna","Siv","Camilla","Iselin","Makka","Eva","Coco"]
fornavn1 = [
    "Adolf",
    "Ariel",
    "Camilla",
    "Coco",
    "Erna",
    "Eva",
    "Gustav",
    "Iselin",
    "Knut",
    "Makka",
    "Marie",
    "Oluf",
    "Siv",
    "Tor",
]
etternavn1 = [
    "Ardvark",
    "Braathen",
    "Cancer",
    "Chanel",
    "Collett",
    "Creosot",
    "Dinglrot",
    "Jensen",
    "Kavli",
    "Kremer",
    "Kvitmyr",
    "Lisdex",
    "Markali",
    "Mecklenburg",
    "Nordhus",
    "Nyremyr",
    "Olsen",
    "Prelltorp",
    "Solberg",
    "Trinkelheim",
    "Werner",
    "Ødegård",
]
# brukernavn1=["Astro","Max","Super","Amfe","Pyro","Baby","Cola","Nitro","Cro","Benzin","MILF-","Pilsy","Mega","Toro","Mora","Mekker","Dekker"]
brukernavn1 = [
    "Amfe",
    "Astro",
    "Baby",
    "Benzin",
    "Cola",
    "Cro",
    "Dekker",
    "MILF-",
    "Max",
    "Mega",
    "Mekker",
    "Mora",
    "Nitro",
    "Pilsy",
    "Pyro",
    "Super",
    "Toro",
]
brukernavn2 = [
    "Plugger",
    "Zuck",
    "boomer",
    "boxer",
    "burner",
    "cola",
    "doofus",
    "fyllik",
    "gamer",
    "kaffi",
    "lick",
    "sneezer",
    "snorter",
    "speed",
    "splash",
    "sport",
    "stormer",
    "vag'n",
    "zoomer",
]

rettighet = "bruker"
# password_hash=generate_password_hash("python",salt_length=200)
def auto_gen_bruker(antall):
    """danner automatisk så mange brukere enn oppgir antall."""
    for x in range(1, antall, 1):
        fornavn = choice(fornavn1)
        etternavn = choice(etternavn1)
        brukernavn = choice(brukernavn1) + choice(brukernavn2) + tid2 + str(x)
        print(brukernavn)
        email1 = choice(fornavn) + "@auto.gen.no"
        passord = "autopython"
        ny_bruker_db(
            fornavn=fornavn,
            etternavn=etternavn,
            brukernavn=brukernavn,
            email1=email1,
            rettighet="Bruker",
            passord=passord,
        )


def post_fil():
    """i static/autodata.p1.txt kan en legge inn dummydata, og dette blir brukt som mal"""
    with open("BLOG/static/autodata/p1.txt", "r", encoding="UTF-8") as f:
        _ant = f.readline()  # fil starter med tall på ant poster
        antall_p = int(_ant)  # konvertere til int siden vi bruker range()
        for runde in range(1, antall_p, 1):  # start,stop,step
            stopp = False
            slug = ""
            innhold = ""
            tittel = f.readline()
            tomt = (
                f.readline()
            )  # dermed kan txt.fil inneholde en blank linje mellom tittel og slug for leselighet

            while stopp == False:  # loop for å lese inn slug
                linje = f.readline()
                if "<>" in linje:  # or linje=="":
                    break  # stopp=True #break
                else:
                    slug = slug + linje
            while stopp == False:  # loop for å lese innhold
                linje = (
                    f.readline()
                )  # readline legger til et /n på slutten av hver string
                if "<>" in linje:
                    break  # stopp=2
                else:
                    innhold = innhold + linje
            print("Tittel:", tittel)
            print("Slug:", slug)
            print("innhold:", innhold)
            l = [2, 3, 4, 5, 6, 7, 8, 9]  # forfatter_id vi knytter post til.
            tilfeldig = choice(l)
            ny_post_db(
                tittel=tittel, slug=slug, forfatter_id=tilfeldig, innhold=innhold
            )
    f.close()