# legges i app root hvis gunicorn skal kjøres som: gunicorn --bind 0.0.0.0:8000 wsgi:Kontroll
# som vil kjøre gunicorn modul fra nginx uten nevneverdig setup av nginx
#(endret default.conf i sites-enabled til LISTEN 8000)

# server {
#   listen 8000 jakob.kentry.no;
#   listen [::]::8000 jakob.kentry.no;
#   root /ny2/venv2;
#    # Add index.php to the list if you are using PHP
#    index.html index-blahah.html 
#  server_name _;
# }
# har ikke satt server navn under server_name og det virket. Om egentlig noe i default trengs å endres på bare for å starte serveren er jeg usikker på.

# --wsgi.py------------- 
#   
from BLOG import Kontroll

if __name__=="__main__":
    Kontroll.run()
# ----------------------wsgi.py EOF

 