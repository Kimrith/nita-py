from flask import render_template
from . import user_bp


@user_bp.route("/contact")
def contact():
    return render_template("front/share/contact.html")