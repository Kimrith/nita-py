from flask import render_template, request, redirect, url_for, flash, session
from model.models import User
from helper import load_users, check_password
from extensions import limiter
from . import admin_bp


@admin_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("2 per minute", methods=["POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Try Database User
        user = User.query.filter_by(email=email).first()
        if user and check_password(password, user.password):
            if user.role != "Admin":
                flash("Access denied. Administrator privileges required.", "danger")
                return redirect(url_for("admin.admin_login"))

            session.clear()
            session.permanent = bool(request.form.get("remember"))
            session["user_id"] = user.id
            session["user_email"] = user.email
            session["admin_logged_in"] = True
            session["username"] = user.fullname or user.email.split("@")[0]
            session["admin_name"] = user.fullname or user.email.split("@")[0]
            session["user_role"] = user.role
            session["role"] = user.role
            flash(f"Welcome to SV7 Admin Control Center, {user.fullname or 'Administrator'}!", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("admin.admin_dashboard"))

        # Fallback to JSON Users
        json_user = load_users().get(email)
        if json_user and check_password(password, json_user.get("password", "")):
            session.clear()
            session.permanent = bool(request.form.get("remember"))
            session["user_id"] = json_user.get("id", 1)
            session["user_email"] = email
            session["admin_logged_in"] = True
            session["username"] = json_user.get("name", "Administrator")
            session["admin_name"] = json_user.get("name", "Administrator")
            session["user_role"] = "Admin"
            session["role"] = "Admin"
            flash("Welcome to SV7 Admin Control Center!", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("admin.admin_dashboard"))

        flash("Invalid administrator credentials. Access denied.", "danger")
        return redirect(url_for("admin.admin_login", next=request.args.get("next")))

    return render_template("admin/login.html")


@admin_bp.route("/logout", methods=["GET", "POST"])
def admin_logout():
    session.clear()
    flash("Successfully signed out from Admin Control Center.", "info")
    return redirect(url_for("admin.admin_login"))
