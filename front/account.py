from flask import render_template
from helper import login_required
from . import user_bp


@user_bp.route("/account")
@login_required
def account():
    return render_template("front/account.html")