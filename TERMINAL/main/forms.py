from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms import PasswordField, BooleanField, SelectField
from wtforms.validators import Email, InputRequired, EqualTo, Length

class MAIN_Questions(FlaskForm):
    navn= StringField(label="navn/org/email:")
    klasse= SelectField(label="Skytter klasse:",validators=[InputRequired(message="Velg en klasse")], choices=[
    ("Klasse 1", "1"),
    ("Klasse 2", "2"),
    ("Klasse 3", "3"),
    ("Klasse 4", "4"),
    ("Klasse 5", "5"), 
    ("Helt egen klasse!", "egen klasse")
    ]
    )
    forslag= TextAreaField(label="Har du noen forslag til endringer/forbedringer?", render_kw={"placeholder": "Hvis jeg tenker etter så føler jeg at...","rows":"8","col":"300","style":"width:600px; heigth:500px"})
    send_knapp=SubmitField(label="SEND SVAR!")


#### VISER HVILKEN FORMS DE ER FRA
# class MAIN_CommentForm(FlaskForm):
#     """(FlaskForm) field_name: innhold, forfatter, send_knapp. ex: reqdata=form.innhold.data"""
#     #innhold = TextAreaField(label="Skriv en kommentar:",validators=[Length(min=10, max=4096, message="Må inneholde %(min)d - %(max)d tegn!")],render_kw={"placeholder": "Jeg husker det var...","rows":"5","col":"300","style":"width:600px; heigth:300px"})
#     innhold = TextAreaField(label="Skriv en kommentar:",validators=[Ugyldig, Lengde(min=10, max=4096)],render_kw={"placeholder": "Jeg husker det var...","rows":"5","col":"300","style":"width:600px; heigth:300px"})
#     forfatter = StringField(label="Hilsen:", default="anonym")
#     send_knapp = SubmitField(label="SEND POST")

# class MAIN_CommentPost(FlaskForm):
#     """debatt innlegg på UserPost"""
#     tittel=StringField(label="Emne:", validators=[Lengde(min=3, max=255)],render_kw={"style":"width:900px; heigth:100px"})
#     innhold=TextAreaField(label="Innhold:", validators=[Lengde(min=5, max=4096)],render_kw={"rows":3,"col":300,"style":"width:900px; heigth:200px"})
#     #post_id
#     #forfatter_id
#     send_knapp=send_knapp=SubmitField(label="POST KOMMENTAR")
# class MAIN_PostForm(FlaskForm):
#     """tittel, slug, innhold, brukernavn(sjekkes mot Brain.bruker), send_knapp"""
#     tittel = StringField(label="Tittel:", validators=[Ugyldig, Lengde(min=5, max=255)],render_kw={"style":"width:900px; heigth:100px"})
#     slug   = TextAreaField(label="Tema/slug:", validators=[Ugyldig, Lengde(min=5, max=500)],render_kw={"rows":3,"col":300,"style":"width:900px; heigth:200px"})
#     innhold= TextAreaField(label="Innhold:", validators=[Ugyldig, Lengde(min=5, max=4096)],render_kw={"placeholder": "Det var en gang...","rows":"5","col":"300","style":"width:900px; heigth:500px"})
#     #brukernavn=StringField(label="Bekr:", validators=[ConfirmUserLogin(message="login required to post!")]) #ConfirmUserName()])
#     #recaptcha=RecaptchaField() #bruker Google
#     send_knapp=SubmitField(label="POST", validators=[ConfirmUserLogin(message="login required!")])


# class USERS_LoginForm(FlaskForm):
#     """brukernavn, password, remember_me, send_knapp"""
#     brukernavn = StringField(label="Brukernavn:", validators=[InputRequired(message= "Skriv inn ditt brukernavn!")])
#     password = PasswordField(label="Password", validators=[InputRequired(message="Fyll inn korrekt passord!")])
#     remember_me = BooleanField('Remember Me', default=False)
#     send_knapp=SubmitField(label="LOGIN")

# class USERS_NyBrukerForm(FlaskForm):
#     """fornavn, etternavn,brukernavn,password,email,valg """
#     fornavn = StringField(label="Fornavn:", validators=[Lengde(min=1, max=40, message="%(min)d - %(max)d tegn!")])
#     etternavn = StringField(label="Etternavn:", validators=[Lengde(min=1, max=40, message="%(min)d - %(max)d tegn!")])
#     brukernavn = StringField(label="Brukernavn:", validators=[Lengde(3, 40, "brukernavn skal inneholde %(min)d - %(max)d tegn!")])
#     password = StringField(label="Passord:", validators=[Lengde(min=4, max=80, message="%(min)d - %(max)d tegn!")])
#     confirm_password = StringField(label='Gjenta passord',validators=[EqualTo(fieldname="password", message='Passord må matche.')])
# #     email = StringField(label='Email', validators=[Email(message='Not a valid email address.'),Lengde(min=4, max=120, message="%(min)d - %(max)d tegn!")])
#     valg = SelectField(label='Jeg er:',validators=[InputRequired(message="Gjør et valg!")],choices=[
#             ('bruker', 'en vanlig bruker'),
#             ('gjestebruker', 'en gjest på besøk'),
#             ('admin', 'en Administrator (må godkjennes av Vokteren)'),
#             ('moderator', 'en Moderator'),
#             ('auto-gen', 'en automatisk opprettet profil'),
#             ('temp', 'en profil som skal slettes')
#         ]
#     )
# #     send_knapp=SubmitField(label="REGISTRER NY BRUKER")

# class USERS_PasswordForm(FlaskForm):
#     password=PasswordField(label="Hvorfor skal du autoriseres?", validators=[InputRequired(message="FEIL!")])

# class USERS_SelectMeldingForm(FlaskForm):
#     """valg:nye,alle,slett"""
#     valg=SelectField(label="VIS MELDINGER",validators=[InputRequired(message="Velg fra menyen")],
#     choices=[('nye',"les nye meldinger"),
#     ('alle','se alle meldinger'),
#     ('slett',"slett leste meldinger"),
#     ])
#     send_knapp=SubmitField(label="UTFØR")

# class USERS_SendMeldingForm(FlaskForm):
#     tittel = StringField(label="Emne:", validators=[Lengde(min=5, max=255)])
#     innhold = TextAreaField(label="Melding:", validators=[Lengde(min=5, max=1024)],render_kw={"placeholder": "Hei!","rows":5,"col":300,"style":"width:600px; heigth:300px"})
#     send_til= StringField(label="Til brukernavn:", default="", validators=[ConfirmUserName(message="finner ikke brukernavn!")])
#     send_knapp=SubmitField(label="SEND")

# class USERS_LocalForm(FlaskForm):
#     tittel = StringField(label="Dag/emne:", validators=[Lengde(min=2, max=255)],render_kw={"style":"width:900px; heigth:100px"})
#     innhold= TextAreaField(label="Innhold:", validators=[Lengde(min=5, max=4096)],render_kw={"placeholder": "Notering","rows":"5","col":"300","style":"width:900px; heigth:500px"})
#     send_knapp=SubmitField(label="SEND")

# print ("FORMS EOF IN",__name__)