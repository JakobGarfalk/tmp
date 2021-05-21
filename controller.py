with open('.env','w') as f:
   f.write('FLASK_APP="BLOG" ')
   f.close()
import wsgi
