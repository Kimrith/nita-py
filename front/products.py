from flask import render_template, request, flash, redirect, url_for
from helper import get_products, get_product, decorate_products
from . import user_bp


@user_bp.route("/products")
def products():
    category = request.args.get("category")
    all_products = decorate_products(get_products())
    products_list = all_products

    if category:
        products_list = [p for p in products_list if p.get("category") == category]

    categories = sorted({p.get("category") for p in all_products if p.get("category")})
    return render_template(
        "front/products.html",
        products=products_list,
        categories=categories,
        active_category=category,
    )


@user_bp.route("/view/<int:product_id>")
@user_bp.route("/product/<int:product_id>")
def product(product_id):
    item = get_product(product_id)
    if not item:
        flash("Product not found. Please try again.")
        return redirect(url_for("user.products"))

    related = decorate_products([
        p
        for p in get_products()
        if p.get("category") == item.get("category") and p.get("id") != item.get("id")
    ][:4])

    return render_template("front/product.html", product=item, related=related)