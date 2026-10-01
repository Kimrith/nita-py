from flask import render_template, request, flash, redirect, url_for
from helper import build_cart_items, send_checkout_notification, redirect_with_cart
from . import user_bp


@user_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = build_cart_items()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        notes = request.form.get("notes", "").strip()

        if not items:
            flash("Your cart is empty.")
            return redirect(url_for("user.cart"))

        send_checkout_notification(name, phone, email, address, notes, items, total)
        flash("Order submitted successfully.")
        return redirect_with_cart(url_for("user.home"), {})

    return render_template("front/checkout.html", items=items, total=total)