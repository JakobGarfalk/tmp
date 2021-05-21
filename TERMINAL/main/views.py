from TERMINAL.main import bp
from flask import render_template, flash
from TERMINAL.main.forms import MAIN_Questions

@bp.route("/", methods=["GET","POST"])
@bp.route("/index/", methods=["GET","POST"])
def main_index():
    title="REX VULNERATUS EST!"
    form=MAIN_Questions()
    html_txt="<head><title>INDEXUS</title></head><body><h1>REX VULNERATUS EST!</h1></body>"
    if form.validate_on_submit():
        navn=form.navn.data
        klasse=form.klasse.data
        text=form.forslag.data
        with open("answers.txt","a",encoding="UTF-8") as f:
            f.writelines(navn)
            f.writelines(klasse)
            f.write(text)
            f.write("--------\n")
            f.close()
        flash ("Tusen takk for hjelpen!")
    return render_template("main/index.html", title=title, form=form)

@bp.route("/shoot/", methods=["GET","POST"])
def main_shoot():
    return "123"

@bp.route("/results/", methods=["GET"])
def main_results():
    return "error"





@bp.route("/shutdown/", methods=["GET","POST"])
def main_shutdown():
    with open("controller.py","w") as f:
        f.write("with open('.env','w') as f:\n")
        f.write("   f.write('FLASK_APP=\"BLOG\" ')\n")
        f.write("   f.close()\n")
        f.write("import wsgi\n")
        f.close()
    print ("file controller made, exit to neutral.py")
    import TERMINAL.neutral
    return "exit terminal"
    