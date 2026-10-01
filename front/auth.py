from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from extensions import db, limiter
from model.models import User
from helper import load_users, save_users, check_password
from . import user_bp


@user_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Try Database User first
        user = User.query.filter_by(email=email).first()
        if user and check_password(password, user.password):
            session.clear()
            session.permanent = bool(request.form.get("remember"))
            session["user_id"] = user.id
            session["user_email"] = user.email
            session["username"] = user.fullname or user.email.split("@")[0]
            session["user_role"] = user.role
            flash("Welcome back!", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("user.account"))

        # Fallback to JSON Users
        json_user = load_users().get(email)
        if json_user and check_password(password, json_user.get("password", "")):
            session.clear()
            session.permanent = bool(request.form.get("remember"))
            session["user_id"] = json_user.get("id", 1)
            session["user_email"] = email
            session["username"] = json_user.get("name", email.split("@")[0])
            session["user_role"] = "Customer"
            flash("Welcome back!", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("user.account"))

        flash("Invalid email or password.", "danger")
        return redirect(url_for("user.login", next=request.args.get("next")))

    return render_template("front/login.html")


@user_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if User.query.filter_by(email=email).first() or email in load_users():
            flash("This email is already registered.", "warning")
            return redirect(url_for("user.register"))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("user.register"))

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "warning")
            return redirect(url_for("user.register"))

        hashed_pwd = generate_password_hash(password)

        # Save to Database Model
        new_db_user = User(
            fullname=name,
            email=email,
            password=hashed_pwd,
            role="Customer",
            status="Active"
        )
        db.session.add(new_db_user)
        db.session.commit()

        # Also backup to JSON users
        users = load_users()
        users[email] = {
            "name": name,
            "email": email,
            "password": hashed_pwd,
        }
        save_users(users)

        session.clear()
        session["user_id"] = new_db_user.id
        session["user_email"] = email
        session["username"] = name
        session["user_role"] = "Customer"
        flash("Account created successfully.", "success")
        return redirect(url_for("user.account"))

    return render_template("front/create-user.html")


@user_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("user.login"))


@user_bp.route("/reset-password", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def reset_password():
    if request.method == "POST":
        flash("Password reset link sent.", "info")
        return redirect(url_for("user.login"))
    return render_template("front/forgot-password.html")