from flask import render_template, request, flash, redirect, url_for
from helper import build_cart_items, get_cart, redirect_with_cart
from . import user_bp


@user_bp.route("/cart")
def cart():
    items, total = build_cart_items()
    return render_template("front/cart.html", items=items, total=total)


@user_bp.post("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    cart = get_cart()
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    flash("Product added to cart.")
    return redirect_with_cart(request.referrer or url_for("user.cart"), cart)


@user_bp.post("/cart/update/<int:product_id>")
def update_cart(product_id):
    action = request.form.get("action")
    cart = get_cart()
    key = str(product_id)

    if key not in cart:
        return redirect(url_for("user.cart"))

    if action == "plus":
        cart[key] += 1
    elif action == "minus":
        cart[key] -= 1
        if cart[key] <= 0:
            cart.pop(key, None)
    elif action == "remove":
        cart.pop(key, None)

    return redirect_with_cart(url_for("user.cart"), cart)


@user_bp.post("/cart/clear")
def clear_cart():
    flash("Cart cleared.")
    return redirect_with_cart(url_for("user.cart"), {})