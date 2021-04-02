#
# bruker custom_login som loginmanager
# gir tilgang til Bruker gjennom
from BLOG.models import Bruker
from BLOG.custom_login.utils import login_user
from BLOG.custom_login import current_user
if current_user.is_authenticated:
    id=current_user.id
    brukernavn=current_user.brukernavn
    # dette hentes via models; Bruker(UserMixin, db.Model)
    # slik at alle egenskaper til Bruker lastes til current_user ved
    bruker_obj=Bruker.query.get(1) #get henter bruker med primary key==1
    login_user(bruker_obj)
    # nå vil bruker_obj ha attributtene;
    current_user.brukernavn==bruker_obj.brukernavn
    #osv, men også få:
    current_user.is_authenticated==True
    current_user
if current_user.is_anonymous:
    current_user.id==0
    current_user.brukernavn==False
    # dette er definert i models; AnonymBruker(AnonymousUserMixin)
"""
config.py
POST_PER_PAGE=2
COMMENTS_PER_PAGE=3
    # disse setter verdien til .pagination som brukes av SQLALCHEMY,
    # variablene kan hete hva som helst, men jeg har ønsket å bruke engelsk vanlig konvensjon.
    # i db_func.py (eller hvor enn paginering skjer) må Kontroll/app.config["POST_PER_PAGE"] benyttes for å hente
    # verdiene.

# Sette verdiene (husk de er ikke globale og må settes i hver funk de brukes!)
config=current_app.config   
    # config er et dict, current_app.config er best når flere verdier skal settes.
COMMENTS_PER_PAGE=config.get("COMMENTS_PER_PAGE",1)
POST_PER_PAGE=config.get("POST_PER_PAGE", 1)
    # eller:
POST_PER_PAGE=Kontroll.config['POST_PER_PAGE'] or 1
"""
# ## fra models:        ### SELF REFERENTIAL RELATIONSHIP
"""
followed = db.relationship( # i Bruker
        'Bruker', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
            ### followers er hjelpe table, den oppføres rett over Bruker klasse.
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')), # venstre siden
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id')) ## høyre siden
)
    ### i view
    if user.brukernavn==current_user.brukernavn:
        form=BekreftForm1()
        form.send_knapp.label.text="LES MELDINGER" # overskriver default label på SubmitButton
        form2=False
        postkasse=False #Meldinger.query.filter_by(send_til=user.id).all()
        follow_me=user.followers.all()
        follow_by=False
    ## i macro / HTML
{% macro bruker_side(bruker, follow_me, follow_by) %}
    <h1>Profil: {{ bruker.brukernavn }} </h1>
    
    <p><small>(ID:{{bruker.id}}, Opprettet : {{bruker.dato.strftime("%H:%M:%S %e.%b.%y")}})</small></p>
    <p>{{bruker.fornavn}} {{bruker.etternavn}}</p>
    {% if follow_me %}
      {% for fm_users in follow_me %}
        <p>Følger: {{fm_users.brukernavn}} </p>
        <a href="/bruker/{{fm_users.brukernavn}}" class="w3-item w3-button"> {{fm_users.brukernavn}}</a>
      {% endfor %}
    {% endif %}
    {% if follow_by %}
      {% for fb_users in follow_by %}
        <p>Fulgt av: {{fb_users.brukernavn}} </p>
        <a href="/bruker/{{fb_users.brukernavn}}" class="w3-item w3-button"> {{fb_users.brukernavn}}</a>
    {% endfor %}
    {% endif %}
    
    <p>Followers: {{ bruker.followers.count() }} følger med, {{ bruker.followed.count() }} følges med på.</p>
    <p>Om meg:  </p>
  
    <p>Sist Aktiv: {{bruker.logindato.strftime("%H:%M:%S %e.%b.%y")}}</p>
"""