from datetime import datetime, timedelta
import unittest
from BLOG import Kontroll as app
from BLOG import db
from sqlalchemy import func
from werkzeug.security import generate_password_hash,check_password_hash
from BLOG.models import Bruker,UserPost
###
### UNIT TESTER
def bruker_fra_db(reqnavn=None, reqID=None):
    """Oppgi reqnavn, ELLER reqID & få returnert Bruker.query.object"""
    
    if not reqnavn==False and not reqnavn==None:
        finnDB1 = (db.session.query(Bruker)
        .filter(func.lower(Bruker.brukernavn) == func.lower(reqnavn))
        .first())        
    if not reqID==None and reqnavn==None:
        _reqID=int(reqID)
        #finnDB1 = (db.session.query(Bruker).filter(Bruker.id==_reqID).first())
        db.session.query(Bruker).get(_reqID)
        return finnDB1
def ny_bruker_db(fornavn="Zoe",etternavn="Quinn",brukernavn="ZoeQu",email1="ZoeQ@local.ho",rettighet="Bruker",passord="python"):
        """oppretter ny bruker, return msg string"""
        password_hash=generate_password_hash(passord, salt_length=200)
    
        prevent_double=bruker_fra_db(reqnavn=brukernavn)
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
            password_hash=password_hash
        )
        # db.session.add(ny)
        # db.session.commit()
        beskjedSTR = "bruker: " + ny.brukernavn + " legges til med ID:" + str(ny.id)
        # flash(beskjedSTR)
        msg = beskjedSTR
        print (msg)
        return ny # returnerer bruker istedenfor i testing
def ny_post_db(tittel, slug, forfatter_id, innhold="Det var en gang"):
    pny1 = UserPost(tittel=tittel,slug=slug,forfatter_id=forfatter_id,innhold=innhold)
    # db.session.add(pny1)
    # db.session.commit()
    return pny1 # return post for testing

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        # u = User(username='susan')
        u = Bruker(fornavn="abc",etternavn="abc",brukernavn='susanna', email1='susan@example.com',rettighet="bruker",password_hash="test")
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    # def test_avatar(self):
    #     u = User(username='john', email='john@example.com')
    #     self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
    #                                      'd4c74594d841139328695756648b6bd6'
    #                                      '?d=identicon&s=128'))
    # def bruker_fra_db(reqnavn=None, reqID=None):
    #     """Oppgi reqnavn, ELLER reqID & få returnert Bruker.query.object"""
    
    #     if not reqnavn==False and not reqnavn==None:
    #         finnDB1 = (db.session.query(Bruker)
    #     .filter(func.lower(Bruker.brukernavn) == func.lower(reqnavn))
    #     .first())
    #     if not reqID==None and reqnavn==None:
    #         _reqID=int(reqID)
    #         #finnDB1 = (db.session.query(Bruker).filter(Bruker.id==_reqID).first())
    #         db.session.query(Bruker).get(_reqID)
    #     return finnDB1
    # def ny_bruker_db(fornavn="Zoe",etternavn="Quinn",brukernavn="ZoeQu",email1="ZoeQ@local.ho",rettighet="Bruker",passord="python"):
    #     """oppretter ny bruker, return msg string"""
    #     password_hash=generate_password_hash(passord, salt_length=200)
    
    #     prevent_double=bruker_fra_db(reqnavn=brukernavn)
    #     if prevent_double != None:
    #         msg = "Brukernavn er allerede i bruk!"
    #         return msg
    #     else:
    #         ny = Bruker(
    #         fornavn=fornavn,
    #         etternavn=etternavn,
    #         brukernavn=brukernavn,
    #         email1=email1,
    #         rettighet=rettighet,
    #         passord="passord saltes og hashes før lagring i databasen",
    #         password_hash=password_hash
    #     )
    #     db.session.add(ny)
    #     db.session.commit()
    #     beskjedSTR = "bruker: " + ny.brukernavn + " legges til med ID:" + str(ny.id)
    #     # flash(beskjedSTR)
    #     msg = beskjedSTR
    #     return msg

    def test_follow(self):
        # u1 = User(username='john', email='john@example.com')
        # u2 = User(username='susan', email='susan@example.com')
        u1 = Bruker(fornavn="abc",etternavn="abc",brukernavn='mistah-johnas', email1='john@example.com',rettighet="bruker",password_hash="test")
        u2 = Bruker(fornavn="abc",etternavn="abc",brukernavn='susannah', email1='susan@example.com',rettighet="bruker",password_hash="test")
        # u3 = Bruker(brukernavn='mari', email1='john@example.com')
        # u4 = Bruker(brukernavn='davidion', email1='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        ##self.assertEqual(u1.followed.first().brukernavn, 'susannah')
        self.assertEqual(u2.followers.count(), 1)
        ##self.assertEqual(u2.followers.first().brukernavn, 'mistah-johnas')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        # u1 = Bruker(brukernavn='mistah-john', email1='john@example.com')
        # u2 = Bruker(brukernavn='susann', email1='susann@example.com')
        # u3 = Bruker(brukernavn='mari', email1='mari@example.com')
        # u4 = Bruker(brukernavn='davidion', email1='davidion@example.com')
        u1 = Bruker(
            fornavn="abc",
            etternavn="abc",
            brukernavn='maister mistah-johnny',
            email1='john@example.com',
            rettighet="bruker",
            passord="passord saltes og hashes før lagring i databasen",
            password_hash="password_hash"
        )
        u2 = Bruker(
            fornavn="abc",
            etternavn="abc",
            brukernavn='susanny',
            email1='susann@example.com',
            rettighet="bruker",
            passord="passord saltes og hashes før lagring i databasen",
            password_hash="password_hash"
        )
        u3 = Bruker(
            fornavn="abc",
            etternavn="abc",
            brukernavn='maria',
            email1='merijeinh@example.com',
            rettighet="bruker",
            passord="passord saltes og hashes før lagring i databasen",
            password_hash="password_hash"
        )
        u4 = Bruker(
            fornavn="abc",
            etternavn="abc",
            brukernavn='davy',
            email1='davvycrack@example.com',
            rettighet="bruker",
            passord="passord saltes og hashes før lagring i databasen",
            password_hash="password_hash"
        )
        # db.session.add(ny)
        # db.session.commit()
        # beskjedSTR1 = "bruker: " + u1.brukernavn + " legges til med ID:" + str(u1.id)
        # beskjedSTR2 = "bruker: " + u2.brukernavn + " legges til med ID:" + str(u2.id)
        # beskjedSTR3 = "bruker: " + u3.brukernavn + " legges til med ID:" + str(u3.id)
        # beskjedSTR4 = "bruker: " + u4.brukernavn + " legges til med ID:" + str(u4.id)
        # # flash(beskjedSTR)
        # msg = beskjedSTR1
        # print(msg)
        # print(beskjedSTR2)
        # print(beskjedSTR3)
        # print(beskjedSTR4)

        # u1 = User(username='john', email='john@example.com')
        # u2 = User(username='susan', email='susan@example.com')
        # u3 = User(username='mary', email='mary@example.com')
        # u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])
        
        beskjedSTR1 = "bruker: " + u1.brukernavn + " legges til med ID:" + str(u1.id)
        beskjedSTR2 = "bruker: " + u2.brukernavn + " legges til med ID:" + str(u2.id)
        beskjedSTR3 = "bruker: " + u3.brukernavn + " legges til med ID:" + str(u3.id)
        beskjedSTR4 = "bruker: " + u4.brukernavn + " legges til med ID:" + str(u4.id)
        # flash(beskjedSTR)
        msg = beskjedSTR1
        print(msg)
        print(beskjedSTR2)
        print(beskjedSTR3)
        print(beskjedSTR4)

        # create four posts
        now = datetime.utcnow()
        # p1 = Post(body="post from john", author=u1,
        #           timestamp=now + timedelta(seconds=1))
        # p2 = Post(body="post from susan", author=u2,
        #           timestamp=now + timedelta(seconds=4))
        # p3 = Post(body="post from mary", author=u3,
        #           timestamp=now + timedelta(seconds=3))
        # p4 = Post(body="post from david", author=u4,
        #           timestamp=now + timedelta(seconds=2))
        p1 = UserPost(tittel="Unit Tester tittel1",slug="nuthin",innhold="post from mistah-john", forfatter_id=u1.id,
                  dato=now + timedelta(seconds=1))
        p2 = UserPost(tittel="Unit Tester tittel2",slug="nuthin",innhold="post from susanal", forfatter_id=u2.id,
                  dato=now + timedelta(seconds=2))
        p3 = UserPost(tittel="Unit Tester tittel3",slug="nuthin",innhold="post from marri-mæ", forfatter_id=u3.id,
                  dato=now + timedelta(seconds=3))
        p4 = UserPost(tittel="Unit Tester tittel4",slug="nuthin",innhold="post from david-ion", forfatter_id=u4.id,
                  dato=now + timedelta(seconds=4))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)