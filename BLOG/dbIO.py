### FIL FOR Å LEKE MED DB - IKKE I BRUK

## from sqlalchemy.sql.schema import DefaultGenerator


from sqlalchemy.sql.functions import current_user
from BLOG import Kontroll, db
from BLOG.DB import engine2, Base2, db_session2

from BLOG.models import Comment, Bruker, UserPost, Dagbok
from BLOG.DB.models import Comment2, Brukere, Poster
from sqlalchemy.orm import query
from sqlalchemy import text, func

query_objekt1 = Comment.query.filter(id == 1).first()

from sqlalchemy import desc
poster=db.session.query(Comment).order_by(desc(Comment.id)).limit(3) #gir siste 3 basert på id

# tran = Comment.query.filter()
signatur="mjauishSs"
finn = db.session.query(Bruker).filter(Bruker.brukernavn.ilike(signatur)).first()
print (finn)

# db_session2.add(tran)
# SELECT table FROM table WHERE søketilstand GROUP_BY column_name HAVING søketilstand
finn = "Admin"
# f = (
#     db.session.query(Bruker)
#     .from_statement(text("SELECT * FROM users WHERE brukernavn=:name"))
#     .params(name=finn)
#     .first()
# )
f3 = (
    db.session.query(Bruker, UserPost)
    .from_statement(text("SELECT * FROM users WHERE brukernavn=:name"))
    .params(name=finn)
    .first()
)
print("post data mangler?: ", f3)
print (f3.Bruker.brukernavn) #men UserPost er slettet/mangler


# - virker:
f1=db.session.query(Bruker,UserPost).join(UserPost).filter(Bruker.brukernavn=='Admin').order_by(UserPost.dato).first()
print (f1.Bruker.brukernavn)
print (f1.UserPost.tittel)
b=Bruker.query.filter_by(brukernavn='Admin').first()
print ("b:",b)
for x in b.post:
    print (x.innhold)

# @Kontroll.route("/bruker/<get_brukernavn>", methods=["GET","POST"])
# @login_required
class current_user():
    brukernavn=""

get_brukernavn="psyhco"
current_user.brukernavn="psycho"
def brukerside(get_brukernavn):
    msg=False
    follow_by=False
    follow_me=False

    if current_user.brukernavn == get_brukernavn: user=current_user
    if current_user.brukernavn != get_brukernavn: user=bruker_fra_db(get_brukernavn)
    
    if user==None: return redirect(url_for('index')) #failsafe
    print ("\ncurrent_user.brukernavn is not get_brukernavn: {0},{1}{2}".format(current_user.brukernavn is not get_brukernavn,current_user.brukernavn,get_brukernavn))
    print ("ISIT? ",current_user.brukernavn is get_brukernavn,current_user.brukernavn,get_brukernavn)
    print ("\ncurrent_user is not get_brukernavn: {}".format(current_user is not get_brukernavn))
    print ("\ncurrent_user.brukernavn != get_brukernavn: {}".format(current_user != get_brukernavn))
    print ("ISIT!=? ",current_user.brukernavn != get_brukernavn,current_user.brukernavn,get_brukernavn)
    print ("ISIT==? ",current_user.brukernavn == get_brukernavn,current_user.brukernavn,get_brukernavn)
    print ("ISIT IS? ",current_user.brukernavn is get_brukernavn,current_user.brukernavn,get_brukernavn)
    print ("ISIT NOT? ",current_user.brukernavn is not get_brukernavn,current_user.brukernavn,get_brukernavn)
    print ("\ncurrent_user != get_brukernavn: {}".format(current_user != get_brukernavn))

# SELECT address.* FROM user
    # JOIN address ON user.id=address.user_id
    # WHERE user.name = :name_1
# f3=db.session.query(UserPost, Bruker).from_statement(text("SELECT poster FROM users WHERE brukernavn:=name")).params(name=finn).first()
# f3=db.session.query(UserPost).select_from(Bruker.postet).join(UserPost.postetAv).filter(Bruker.Brukernavn=='Admin')
            #  join(User.addresses).\
            #     filter(User.name == 'ed'), f3.UserPost.tittel

# for x in f3.id:
# print(f3.innhold)
# finn = finn.lower()
# lowercase for begge uten tilpasning, import func:
# f2 = Bruker.query.filter(func.lower(Bruker.brukernavn) == func.lower(finn)).first()

# print(f)
# print(f.__tablename__)
# print("med lower:", f2)
# f.__tablename__ = "brukere"

# print(query_objekt1)

# q = query_objekt1


# class Transfer(object):

#     id = Comment2.id
#     dato = Comment2.dato
#     innhold = Comment2.innhold
#     forfatter = Comment2.forfatter

#     def __init__(self, id, dato, innhold, forfatter):
#         self.id = id
#         self.dato = dato
#         self.innhold = innhold
#         self.forfatter = forfatter


# dette skal kopiere over tables, deretter kan en sende data
# table = Table('test_table', metadata, autoload=True, autoload_with=db1)
# table.create(engine=db2)


x = input(":-")
if x == "q" or x == "e":
    exit()