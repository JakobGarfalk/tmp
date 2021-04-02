#from BLOG.UNIT.config import SQLALCHEMY_DATABASE_TEST
from datetime import datetime, timedelta
import unittest
import os
#from config import konfigdir
#BLOGDIR=os.path.join(konfigdir, "BLOG")
cwd = os.getcwd()

# Print the current working directory
print("Current working directory: {0}".format(cwd))
#from BLOG import Kontroll, db
from BLOG.UNIT import app_test, db
from BLOG.models import Bruker, UserPost

class UserModelCase(unittest.TestCase):
    def setUp(self):
        
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = Bruker(brukernavn='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    # def test_avatar(self):
    #     u = Bruker(username='john', email='john@example.com')
    #     self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
    #                                      'd4c74594d841139328695756648b6bd6'
    #                                      '?d=identicon&s=128'))

    def test_follow(self):
        u1 = Bruker(brukernavn='john', email1='john@example.com')
        u2 = Bruker(brukernavn='susan', email1='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.vennskap.all(), [])
        self.assertEqual(u1.vennskap.all(), [])

        u1.bli_venn(u2)
        db.session.commit()
        self.assertTrue(u1.er_venn(u2))
        self.assertEqual(u1.vennskap.count(), 1)
        self.assertEqual(u1.vennskap.first().username, 'susan')
        self.assertEqual(u2.venner.count(), 1)
        self.assertEqual(u2.venner.first().username, 'john')

        u1.fjern_venn(u2)
        db.session.commit()
        self.assertFalse(u1.er_venn(u2))
        self.assertEqual(u1.vennskap.count(), 0)
        self.assertEqual(u2.venner.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = Bruker(brukernavn='john', email1='john@example.com')
        u2 = Bruker(brukernavn='susan', email1='susan@example.com')
        u3 = Bruker(brukernavn='mary', email1='mary@example.com')
        u4 = Bruker(brukernavn='david', email1='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = UserPost(innhold="post from john", forfatter_id=u1.id,
                  dato=now + timedelta(seconds=1))
        p2 = UserPost(innhold="post from susan", forfatter_id=u2.id,
                  dato=now + timedelta(seconds=4))
        p3 = UserPost(innhold="post from mary", forfatter_id=u3.id,
                  dato=now + timedelta(seconds=3))
        p4 = UserPost(innhold="post from david", forfatter_id=u4.id,
                  dato=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.bli_venn(u2)  # john follows susan
        u1.bli_venn(u4)  # john follows david
        u2.bli_venn(u3)  # susan follows mary
        u3.bli_venn(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.venn_poster().all()
        f2 = u2.venn_poster().all()
        f3 = u3.venn_poster().all()
        f4 = u4.venn_poster().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)