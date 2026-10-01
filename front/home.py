from flask import render_template
from helper import get_products, decorate_products
from . import user_bp


@user_bp.route("/")
def home():
    products = decorate_products(get_products())
    return render_template("front/index.html", products=products)