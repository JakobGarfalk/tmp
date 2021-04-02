"""views/router, pr nå brukes også MethodView, dette skal i egen fil for klarhet"""
### imports fra init:
from BLOG.custom_login.utils import fresh_login_required, login_fresh
from BLOG import Kontroll, db
from BLOG import login_man
### imports fra flask:
from flask import request, render_template, redirect, jsonify
from flask import flash, url_for, make_response, session, escape
from flask import has_request_context
from flask.views import MethodView
from flask.globals import g

### werkzeug er en del av flask:
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse

### import for db kontroll ext:
from sqlalchemy import text, select,desc,func
from sqlalchemy.orm import query
from flask_sqlalchemy import (
    SQLAlchemy,
)  # Flask Sqlalchemy lager automatisk sessionmaker,session, create_engine, mm.
#from flask_login import current_user, login_user, logout_user, login_required
from BLOG.custom_login import current_user,login_user,logout_user,login_required

### imports fra standard lib eller system:
import os
from datetime import datetime
from random import choice
###imports fra BLOG moduler:
from BLOG.models import Comment, Bruker, UserPost, Dagbok, Meldinger
#from BLOG import models
# from BLOG.models import load_user
from BLOG.forms import CommentForm1, LoginForm, NyBrukerForm1, BekreftForm1, PostForm1, SendMeldingForm1

from BLOG.db_func import bruker_fra_db, les_poster,ny_bruker_db, les_comments, send_melding, ny_post_db
#from BLOG.manager import 
##### midlertidige imports legges her, ved feil slett:
from BLOG.forms import ContactForm

## ERROR HÅNDTERING - HØRER DETTE HJEMME I VIEWS?
@Kontroll.errorhandler(404)
def not_found_error(error):
    return render_template("404_feil.html",title="UGYLDIG ADDRESSE")

@Kontroll.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error/500_feil.html',title="CRASH & BURN")
### ------------

####------- KLASSER
class Register:
    """Holde på globale i views variabler"""
    vil_bruker_lagre=0
    trygg_bruker=0
    postkasse=False
 
## from functools import wraps
## from flask import request, redirect, url_for, flash
## krever også Brain objektet
# def login_required(func):
#     @wraps(func)    # wrapper for funksjon
#     def krev_login(*args,**kwargs): # decorator    
#         print ("krever login")
#         if Brain.bruker==False:
#             print ("ikke logget inn") # for at next skal huskes må det integreres i form på login så det plukkes opp i en req.methPOST
#             ## <input type="hidden" value="{{ request.args.get('next', '') }}"/>
#             flash("Du må være logget inn for å besøke den siden!")
#             return redirect(url_for('login1', next=request.url))
#         return func(*args,**kwargs)
#     return krev_login
from BLOG.custom_login.utils import login_url, set_login_view
#


# @Kontroll.login_manager.unauthorized_handler
# def unauth_handler():
#     dato=datetime.utcnow()
#     referanse="UNAUT."+str(dato) # tid loggføres automatisk, men microsec forskjell gjør at log tid, og ref tid er ulik.
#     ip_add_bruker="IP_ADD="+str(request.remote_addr) # ved å oppgi ref_tid kan en nå søke på ms i logfil for å finne hendelsen
#     refnavn="c_u="+str(current_user.brukernavn)
#     my_str=str(request.full_path)+referanse+refnavn+ip_add_bruker
#     Kontroll.logger.info(msg="Ugyldig aut:"+my_str)
#     return render_template("bruker/ugyldig_aut.html",error=referanse)

### opprette nye poster automatisk, eller brukere.
#from BLOG.db1 import post_fil
#post_fil()

db.create_all()
print("Laster Views...")

## GLOBALS med local scope:
msg=False
postkasse=False

#@Kontroll.before_first_request
#def before_first_req():
#     Register.vil_bruker_lagre=0

# før hvert request - altså hver eneste GET osv
lock_entry=False
@Kontroll.before_request
def before_req():
    """før hver request lastes brukernavn via Brain.load()"""
    if lock_entry:
        if Register.trygg_bruker==0:
        #if request.args
            if request.method=="POST":
                if request.form["revelation"]=="thereburns_theredie_theregrow":
                    Register.trygg_bruker=5
        
            return render_template("dev/front.html", title="What Are You?")
    if current_user.is_authenticated:
        print ("logget inn som:",current_user.brukernavn)


# må sendes en response, og return
# @Kontroll.after_request
# def afterfunk(response):
#    print ("after req")
#    return response


# --- Server admin:


# ------INIT VIEWS SERVER NORMAL:
@Kontroll.shell_context_processor  # Flask kjenner igjen denne hvis vi kjører "FLASK SHELL" i terminal
def make_shell_context():
    from BLOG import models
    ### opprette nye poster automatisk, eller brukere.
    #from BLOG.db1 import post_fil, auto_gen_bruker

    return {"db": db, "Bruker": Bruker, "Post": UserPost, "Comment":Comment, "Meldinger": Meldinger}


# ---Views:---------------------------VIEWS--------------------
# @Kontroll.route("/")
# @Kontroll.route("/index/")
# def index():
#     print("INDEX")
#     Brain.load()  # Brain.bruker oppdatert fra session
#     # from BLOG.DB.models import query_objekt1
#     # poster = query_objekt1
#     poster = db.session.query(Comment).all()
#     # poster = db_session.query(Comment).all()
#     # db_session.remove()
#     hentBrukerStr1 = (
#         Brain.bruker
#     )  # husk at dette blir en verdi(false/str), ikke et objekt el. dikt!
#     print("-indx-Hentet fra obj til str:", hentBrukerStr1)

#     return render_template(
#         "bruker/index.html",
#         title="HOME",
#         bruker=hentBrukerStr1,
#         poster=poster,
#     )



class IndexView(MethodView):
    # poster = db.session.query(Comment).all() #vil da ikke oppdateres før neste session
    def __init__(self):
        q=Bruker.query.filter(Bruker.id>0).count()
        #a=q.count()>0
        #q.count()
        print (f"\n Query Count type={type(q)}, Count={str(q)}")
        self.brukernavn = current_user.brukernavn
        self.page= request.args.get('page', 1, type=int)
        #self.comments=db.session.query(Comment).order_by(desc(Comment.id)).limit(3) #gir siste 3 basert på id
        self.comments=les_comments(limit=3,page=request.args.get('page', 1, type=int))
        self.poster = les_poster()
        #self.template={template:"bruker/index.html",title:"HOME",brukernavn:self.brukernavn,comments1:self.comments,poster:self.poster}
        print ("\n current_user.is_admin={}".format(current_user.is_admin))
    def post(self):
        return redirect(url_for('index'))

    def get(self):
        #page = request.args.get('page', 1, type=int)
        next_url = url_for('index', page=self.comments.next_num) if self.comments.has_next else None
        prev_url = url_for('index', page=self.comments.prev_num) if self.comments.has_prev else None
        
        return render_template(
            "bruker/index.html",
            title="HOME",
            brukernavn=self.brukernavn,
            comments1=self.comments.items,
            poster=self.poster,
            next_url=next_url, prev_url=prev_url
        )
Kontroll.add_url_rule("/", view_func=IndexView.as_view("index"))

##----TMP                           ---##
@Kontroll.route("/tmp/")
def tmpview1():
    t="a=1; b=2; print ('from bytecode',a+b)"
    x=compile(t,mode='exec',filename="ttt")
    exec(x)
    #from INTOLERATE.intolerate_views import intolerate_gate
    #return INTOLERATE.intolerate_views
    #import INTOLERATE.intolerate_views
    #exec(INOLERATE.intolerate_views)
    #return redirect(url_for('intolerate_gate'))
    return render_template("dev/front.html", title="Utviklings side")

@Kontroll.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    poster = Comment.query.order_by(Comment.dato.desc()).paginate(
        page, Kontroll.config['POST_PER_PAGE'], False)
    next_url = url_for('explore', page=poster.next_num) if poster.has_next else None
    prev_url = url_for('explore', page=poster.prev_num) if poster.has_prev else None
    
    return render_template("bruker/index.html", title='Explore', poster=False, comments1=poster.items,
        next_url=next_url, prev_url=prev_url)
#### ------ --                          ---- UTVIKLE

#### --------------- BRUKER SIDE VIEWS: #
@Kontroll.route("/bruker/<get_brukernavn>", methods=["GET","POST"])
@login_required
def brukerside(get_brukernavn):
    msg=False
    follow_by=False
    follow_me=False

    if current_user.brukernavn == get_brukernavn: user=current_user
    if current_user.brukernavn != get_brukernavn: user=bruker_fra_db(get_brukernavn)
    
    if user==None: return redirect(url_for('index')) #failsafe
    # print ("\ncurrent_user.brukernavn is not get_brukernavn: {0},{1}{2}".format(current_user.brukernavn is not get_brukernavn,current_user.brukernavn,get_brukernavn))
    # print ("ISIT? ",current_user.brukernavn is get_brukernavn,current_user.brukernavn,get_brukernavn)
    # print ("\ncurrent_user is not get_brukernavn: {}".format(current_user is not get_brukernavn))
    # print ("\ncurrent_user.brukernavn != get_brukernavn: {}".format(current_user != get_brukernavn))
    print ("ISIT!=? ",current_user.brukernavn != get_brukernavn,current_user.brukernavn,get_brukernavn)
    print ("ISIT==? ",current_user.brukernavn == get_brukernavn,current_user.brukernavn,get_brukernavn)
    print ("ISIT IS? ",current_user.brukernavn is get_brukernavn,current_user.brukernavn,get_brukernavn)
    print ("ISIT NOT? ",current_user.brukernavn is not get_brukernavn,current_user.brukernavn,get_brukernavn)
    # print ("\ncurrent_user != get_brukernavn: {}".format(current_user != get_brukernavn))

    
    if user.brukernavn==current_user.brukernavn:
        form=BekreftForm1()
        form.send_knapp.label.text="LES MELDINGER" # overskriver default label på SubmitButton
        postkasse=False #Meldinger.query.filter_by(send_til=user.id).all()
        follow_by=user.followed.all() ## followed; en var for db.rel (egentlig et query)
        follow_me=user.followers.all() ## followers er en backref
        print (f"\nfollow(ed)_by(_me):{follow_by}")
        print (f"follow(s)_me:{follow_me} \n")
    else:
        postkasse= False
        form=SendMeldingForm1()
        form.send_til.data=user.brukernavn
        form2=False
        #form2.send_knapp.label.text="FØLG"
    print ("\n --",postkasse)
    
    print ("\n user.b:",user.brukernavn)
    # form=SendMeldingForm1()
    # form.send_til.data=user.brukernavn
    # if form2!=False and form2.validate_on_submit() and user.brukernavn!= current_user.brukernavn and form2.form_id.id=="tagged1":
    #     #jeg=bruker_fra_db(reqID=current_user.id)
    #     flashmsg="Du følger ikke med på noenting!"
    #     if current_user.is_following(user)==1:
    #         current_user.unfollow(user)
    #         #flash("Du har sluttet å følge")
    #         flashmsg="Du har sluttet å følge "+str(user.brukernavn)
    #     elif current_user.is_following(user)==0:
    #         current_user.follow(user)
    #         flashmsg="Du følger nå "+str(user.brukernavn)
        
    #     # current_user.bli_venn(user)
        
        # db.session.commit()
        
        # flash (flashmsg)
        # return redirect(url_for("brukerside",get_brukernavn=get_brukernavn))
    if form.validate_on_submit() and user.brukernavn == current_user.brukernavn:
        postkasse=Meldinger.query.filter_by(send_til=user.id, lest="ikke lest").all()

    if form.validate_on_submit() and user.brukernavn != current_user.brukernavn:
        tittel=form.tittel.data
        innhold=form.innhold.data
        til_bruker_def=form.send_til.default
        print ("def_",til_bruker_def)
        til_bruker=form.send_til.data # dette valideres i forms.py
        til_bruker_id=form.objekt_id # skaper denne attributt ved validering i forms.py
        fra_bruker=int(current_user.id)
        #til=db.session.query(Bruker).filter(func.lower(Bruker.brukernavn)==func.lower(til_bruker)).first()
        x=form.objekt_id 
        ## hvis form valideres korrekt får det egenskapen objekt_id (som inneholder til_bruker.id)
        print ("\nFORM OBJEKT_ID ble overført som:{}".format(form.objekt_id))
        #til_obj=bruker_fra_db(reqnavn=til_bruker)
        # if til_obj==None: ##dobbel validering gjør det bare tregere
        #     print ("WTF? Skulle vært validert i form allerede?")
        send_melding(tittel=tittel, innhold=innhold,forfatter_id=fra_bruker,send_til_id=til_bruker_id)
        #m1=Meldinger(tittel=tittel, innhold=innhold,forfatter_id=fra_bruker,send_til=til_obj.id)
        #db.session.add(m1)
        #db.session.commit()
        msg="Melding til {0} er sendt!".format(til_bruker)
    return render_template("bruker/bruker_id.html",bruker=user, form=form, postkasse=postkasse, msg=msg, follow_me=follow_me , follow_by=follow_by)
@Kontroll.route('/bruker/<get_brukernavn>/follow/')
@login_required ### det er bare å glemme å sende bruker objekt til funksjonen. Det kan gå an,
def followbruker(get_brukernavn): ## men ettersom hvert nye view er frem-tilbake mellom bruker:server
    user=bruker_fra_db(get_brukernavn) # spørs det om en engang ønsker å gjøre det.
    # en har i realiteten 2 valg; lagre objektet hos brukeren i en cookie,
    # eller lagre det server-side som user allerede er.
    # at en da må hente frem user obj fra db "unødvendig ofte" er den korrekte måten å håndtere dette på.
    if current_user.is_following(user)==1:
        current_user.unfollow(user)
        #flash("Du har sluttet å følge")
        #flashmsg="Du har sluttet å følge "+str(user.brukernavn)
        flash(f"Du har nå sluttet å følge profil: {user.brukernavn}")
    elif current_user.is_following(user)==0:
        current_user.follow(user)
        # flashmsg="Du følger nå "+str(user.brukernavn)
        flash (f"Du følger profil: {user.brukernavn}")
        db.session.commit()
        # flash (flashmsg)
    return redirect(url_for("brukerside",get_brukernavn=get_brukernavn))

@Kontroll.route("/bruker/<get_brukernavn>/meldinger/", methods=["GET","POST"])
@login_required
def bruker_meldinger_view(get_brukernavn):
    if not current_user.brukernavn==get_brukernavn:
        return redirect(url_for('login_bruker_view'))
    #msg=False
    form=False
    postkasse=False
    form=SendMeldingForm1()
    
    # etter å sikre at current_user stemmer med brukersiden vi faktisk viser,
    #user=bruker_fra_db(get_brukernavn) # trenger vi hente bruker?
    user=current_user #? nei vi gjør ikke det.
    #postkasse=Meldinger.query.filter_by(send_til=user.id).all()
    if form.validate_on_submit() and user.brukernavn == current_user.brukernavn:
        postkasse=Meldinger.query.filter_by(send_til=user.id).all()

    return render_template("bruker/bruker_id.html",postkasse=postkasse,msg=msg,bruker=user)
#brukerside_dict={"msg":False,"follow_by":False,"follow_me":False} 
@Kontroll.route("/bruker/<get_brukernavn>/siste_post",methods=["GET","POST"])
@login_required
def bruker_post(get_brukernavn):
    brukerside_dict={"msg":False,"follow_by":False,"follow_me":False} 
    msg=False
    follow_by=False
    follow_me=False
    user=bruker_fra_db(get_brukernavn)
    post=UserPost.query.filter(UserPost.forfatter_id==current_user.id).order_by(UserPost.dato.desc()).first()
    if user.brukernavn==current_user.brukernavn and post!=None:
        form=PostForm1()
    else:
        form=False
    if form!=False and form.validate_on_submit():
        print ("\n OK! \n")

    if user==None: # dersom bruker ikke eksisterer el URL møkk.
        return redirect(url_for('index'))
    #siste=UserPost.query.filter(UserPost.forfatter_id==current_user.id).order_by(UserPost.dato.desc()).first()
    if form!=False and request.method=="GET":
        form.brukernavn.data=user.brukernavn
        form.tittel.data=post.tittel
        form.slug.data=post.slug
        form.innhold.data=post.innhold
    return render_template("bruker/bruker_post.html",bruker=user,msg=msg,poster=post,form=form,follow_by=follow_by,follow_me=follow_me)

@Kontroll.route("/bruker/rediger_profil/",methods=["GET","POST"])
@fresh_login_required
def redigere_profil():
    
    # if form.validate_on_submit():
    #     pass
    # #      current_user.username = form.username.data
    # #     current_user.about_me = form.about_me.data
    # #     db.session.commit()
    # #     flash('Your changes have been saved.')
    # #     return redirect(url_for('edit_profile'))
    # elif request.method == 'GET':
    #     pass
    #     form.username.data = current_user.username
    #     form.about_me.data = current_user.about_me
    return render_template('bruker/dagbok.html', title='Edit Profile')

#### #####                          ------
@Kontroll.route('/login/', methods=['GET', 'POST'])
def login_bruker_view():
    user=None
    lyd1=choice(seq=[True,False,True,False,False])
    if current_user.is_authenticated:
        flash(f"Du er allerede logget inn som: {current_user.brukernavn}") #return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Bruker.query.filter(func.lower(Bruker.brukernavn)==func.lower(form.brukernavn.data)).first()
        print (user)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login_bruker_view'))
        #JaNei=login_user(user)
        if login_user(user)==True:
            flash(f"Logget inn med ID: {current_user.id} , {current_user.brukernavn}")
            user.logindato = datetime.utcnow()
            user.passord = "ditt passord er saltet og hashet"
            db.session.add(user)  # login_db)
            db.session.commit()
        #, remember=False)#form.remember_me.data)
        next_page = request.args.get('next')
        ## legges til med validering av korrekt side next_page
        #if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('index')
        # return redirect(next_page)
        #return redirect(url_for('index'))
    return render_template('bruker/login.html', title='Sign In', form=form, bruker=user, lyd1=lyd1)


@Kontroll.route("/kon/", methods=["GET", "POST"])
def kontakt_tmp():
    """Standard `contact` form."""
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("kontakt.html", form=form, template="form-template")


@Kontroll.route("/contact/", methods=["GET", "POST"])
def contact():
    """Standard `contact` form."""
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("contact.jinja2", form=form, template="form-template")


@Kontroll.route("/logout/")
@login_required
def logout1():
    print (current_user.brukernavn)
    logout_user()
    print (current_user.id)
    print (current_user.brukernavn)
    flash("Du er logget ut!")
    return redirect(url_for("index"))


# @Kontroll.route("/kommentarer/", methods=["GET", "POST"])
@Kontroll.route("/kommenter/", methods=["GET", "POST"])
def kommenter():
    #poster = Comment.query.all()
    #comments1=db.session.query(Comment).order_by(desc(Comment.id)).all() #vis siste først
    msg = False

    form = CommentForm1()

    if form.validate_on_submit():  # form er gyldig & method=POST

        innhold = form.innhold.data  # henter data fra FlaskForm
        forfatter = form.forfatter.data
        comment = Comment(innhold=innhold, forfatter=forfatter)
        if current_user.is_anonymous:
            flash("Ettersom du ikke er logget inn, går denne prossesen noe tregere...")

        
        
        if innhold == "":
            msg = "Det har skjedd en feil i validering av kommentar skjemaet."
            # LogBug -> opprett en loggerDobbel validering for dette???
        #if forfatter == "anonym" or forfatter == "":
            #flash("Usignerte kommentarer postes som anonym")
        
        print("ID", comment.id)

        db.session.add(comment)
        db.session.commit()
        msg="Din kommentar er lagret!"
    #comments1=les_comments(limit=10) # på denne måten ser vi siste postede også
                                    # unngår post-lag-delay effekt
    page = request.args.get('page', 1, type=int)
    #comments1 = Comment.query.order_by(Comment.dato.desc()).paginate(page, Kontroll.config['POST_PER_PAGE'], False)
    comments1=les_comments(page=page)
    next_url = url_for('kommenter', page=comments1.next_num) if comments1.has_next else None
    prev_url = url_for('kommenter', page=comments1.prev_num) if comments1.has_prev else None
    paginated_comments=comments1.items
    return render_template(
        "bruker/kommenter.html",
        title="Arkivarium",
        comments1=paginated_comments,
        msg=msg,
        form=form,next_url=next_url,prev_url=prev_url
    )


@Kontroll.route("/innlegg/", methods=["GET", "POST"])
@Kontroll.route("/poster/", methods=["GET", "POST"])
def innlegg():
    msg = False
    form=PostForm1()
    #poster = UserPost.query.all()
    req_side = request.args.get('page', 1, type=int)
    poster = les_poster(page=req_side)
    #husk at pagination objects må sendes som post.items for å kunne itereres i templat
    #Comment.query.order_by(Comment.dato.desc()).paginate(
     #   page, Kontroll.config['POST_PER_PAGE'], False)
    next_url = url_for('innlegg', page=poster.next_num) if poster.has_next else None
    prev_url = url_for('innlegg', page=poster.prev_num) if poster.has_prev else None

    if form.validate_on_submit():
        tittel=form.tittel.data
        slug=form.slug.data
        innhold=form.innhold.data
        forfatter=form.brukernavn.data # forfatter sjekkes mot Brain.BrukerID i form validering
        print ("DEBUG:",forfatter,"-form.field. & Session_ID",current_user.id)
        
        ny = UserPost(tittel=tittel, slug=slug, forfatter_id=int(current_user.id), innhold=innhold
            )
        db.session.add(ny)
        db.session.commit()
        
        msg = "Innlegget er nå lagret i arkivet."

    return render_template(
        "bruker/poster.html", title="POSTER", poster=poster.items, msg=msg, form=form,brukernavn=current_user.brukernavn,
        next_url=next_url,prev_url=prev_url
    )
@Kontroll.route('/poster/kommentarer/<get_post>',methods=["GET","POST"])
def post_comment(get_post):
    post=UserPost.query.get(int(get_post))
    return render_template("bruker/post_com.html",poster=post)

@Kontroll.route("/admin/", methods=["GET", "POST"])
@login_required
def adminfunksjon():
    finnDB = False
    finnPost = False
    msg = False
    if current_user.is_admin:
        msg="Du er ADMIN"
    else:
        msg="Du er ingen admin!"
    # if request.method == "GET":
        
    #     beskjed = "I am the Zentinel. What is your function?"
    #     return render_template("dev/admin.html", title="ADMIN", beskjed=beskjed)
        
    return render_template(
            "dev/admin.html",
            title="ADMIN",
            poster=Comment.query.all(),
            brukere=Bruker.query.all(),
            oppdrag=finnDB, msg=msg
        )

    if request.method == "POST":
        if (
            "submitfunc" in request.form
        ):  # sjekke navn på submit knapp siden det er flere forms på siden.
            if request.form["admin1"] == "alpha omega":
                Brain.admin = True
                redirect(url_for("adminfunksjon"))
        if Brain.admin == False:
            beskjed = "your existence is unclear to us"
            return render_template(
                "dev/admin.html",
                title="ADMIN",
                beskjed=beskjed,
                lyd="spillervoicestayawaymp3",
            )
        if "submit2" in request.form:
            if request.form["Lbrukernavn"] == "":
                msg = "EMPTY SEARCH FIELD!"

            if request.form["Lbrukernavn"] != "":
                reqnavn = request.form["Lbrukernavn"]
                finnDB = Bruker.query.filter(Bruker.brukernavn == reqnavn).first()
                if finnDB != None:
                    # finnPost = UserPost.query.filter(
                    #     UserPost.forfatter_id == finnDB.id
                    # ).all()
                    finnPost = finnDB.poster
                else:
                    msg = "fant ingen slik bruker i DB!"
        return render_template(
            "dev/admin.html",
            title="ADMIN",
            poster=Comment.query.all(),
            brukere=Bruker.query.all(),
            oppdrag=finnDB,
            oppdrag2=finnPost,
            msg=msg,
        )


@Kontroll.route("/nybruker/", methods=["GET", "POST"])
def nybruker():
    brukernavn = current_user.brukernavn  # sjekke session for minBruker
    msg = False
    #bruker = hentBruker_db(Brain.bruker, Brain.brukerID)
    form=NyBrukerForm1()
    
    if form.validate_on_submit():
        fornavn=form.fornavn.data
        etternavn=form.etternavn.data
        brukernavn2=form.brukernavn.data
        passord=form.password.data
        email=form.email.data
        valg=form.valg.data
        msg = ny_bruker_db(fornavn=fornavn,etternavn=etternavn,brukernavn=brukernavn2,passord=passord,email1=email,rettighet=valg)

    return render_template(
        "bruker/nybruker.html",
        title="REGISTRERING",
        bruker=current_user,
        msg=msg,
        brukernavn=brukernavn, form=form)


@Kontroll.route("/dagbok/")
def dagbok():
    
    finnDB1 = False
    
    # if not session.get('minBruker')==None and not session.get('minBrukerID')==None:
    #     print ("-->logger inn fra session...")
    #     hentBruker=Brain.bruker
    #     hentBrukerID=Brain.brukerID
    #     print ("-->---< henter fra db---->>>")
    #     finnDB1=Bruker.query.filter(Bruker.brukernavn==hentBruker, Bruker.id==hentBrukerID).first()

    return render_template("bruker/dagbok.html", title="DAGBOK", bruker=current_user)


class SimpleComment(MethodView):
    """/kommentarer /arkivarium"""

    comments = Comment.query.all()  # da blir den konstant resten av session
    msg = False

    def __init__(self):
        self.poster = (
            SimpleComment.poster
        )  # selv med oppdatering av klasse verdi blir en liggende en request etter
        self.comments = Comment.query.all()  # forespørsel til DB for hvert request
        self.msg = SimpleComment.msg
        
        self.form = CommentForm1()

    def get(self):
        """ Responds to GET requests """
        form = self.form
        return render_template(
            "bruker/kommenter.html",
            title="Arkivarium",
            comments=self.comments,
            msg=self.msg,
            brukernavn=self.brukernavn,
            form=self.form,
        )

    def post(self):
        """ Responds to POST requests """

        form = self.form
        kanLagre = False
        if form.validate_on_submit():
            comment= Comment(innhold=form.innhold.data, forfatter=form.forfatter.data)
            kanLagre=True
            print(comment)
        
        if form.forfatter.data == "" or form.forfatter.data=="anonym":
            flash("Kommentaren postes anonymt.")
        if kanLagre == True:
            db.session.add(comment)
            db.session.commit()
            print("ID", comment.id)
            self.comments = (
                Comment.query.all()
            )  # gir umiddelbar oppdatering, men forlater en siden og kommer tilbake i samme session,
            # så vil, hvis en bruker klasse var, ikke se de nye postene.

        # if self.form.validate_on_submit():
        #     flash('Postet: {}, av:{}'.format(
        #     self.form.contents, self.form.forfatter))

        return render_template(
            "bruker/kommenter.html",
            title="Arkivarium",
            comments=self.comments,
            msg=self.msg,
            brukernavn=self.brukernavn,
            form=self.form,
        )
Kontroll.add_url_rule("/kommentarer/", view_func=SimpleComment.as_view("kommentarer"))
