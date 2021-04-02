###
### ### ### test fil
###

import datetime
from BLOG import login_man
from BLOG.custom_login import current_user
from BLOG.models import Comment, Bruker
from flask.views import MethodView
from flask import render_template,request,flash
from BLOG import Kontroll,db
from BLOG.models import Comment

@Kontroll.login_manager.unauthorized_handler
def unauth_handler():
    dato=datetime.utcnow()
    referanse="UNAUT."+str(dato) # tid loggføres automatisk, men microsec forskjell gjør at log tid, og ref tid er ulik.
    ip_add_bruker="IP_ADD="+str(request.remote_addr) # ved å oppgi ref_tid kan en nå søke på ms i logfil for å finne hendelsen
    refnavn="c_u="+str(current_user.brukernavn)
    my_str=str(request.full_path)+referanse+refnavn+ip_add_bruker
    Kontroll.logger.info(msg="Ugyldig aut:"+my_str)
    return render_template("bruker/ugyldig_aut.html",error=referanse)


class SimpleComment(MethodView):
    """ Example of a class inheriting from flask.views.MethodView 
    
    All 5 request methods are available at /api/example/<entity>
    """
    poster=Comment.query.all()
    msg=False
    def __init__(self):
        self.poster = SimpleComment.poster
        self.msg = False
    def get(self):
        """ Responds to GET requests """
        return render_template("bruker/kommenter.html", title="Arkivarium", poster=self.poster, msg=self.msg)

    def post(self):
        """ Responds to POST requests """
        # if x=="ok":
        #     self.poster=Comment.query.all()
        kanLagre = False
        comment = Comment(
        innhold=request.form["contents"], forfatter=request.form["forfatter"])
        print(comment)
        if request.form["contents"] == "":
            msg = "COMMENT FIELD IS EMPTY!!!"

        else:
            kanLagre = True
        if request.form["forfatter"] == "":
            flash("Så du skriver anonymt?")
        if kanLagre == True:
            db.session.add(comment)
            db.session.commit()
            print("ID", comment.id)
            SimpleComment.poster=Comment.query.all()
        return render_template("bruker/kommenter.html", title="Arkivarium", poster=self.poster, msg=self.msg)

    def put(self):
        """ Responds to PUT requests """
        return "Responding to a PUT request"

    def patch(self, entity):
        """ Responds to PATCH requests """
        return "Responding to a PATCH request"

    def delete(self, entity):
        """ Responds to DELETE requests """
        return "Responding to a DELETE request"

Kontroll.add_url_rule("/api/kommenter", view_func=SimpleComment.as_view("/api/kommenter"))