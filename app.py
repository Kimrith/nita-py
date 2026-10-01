from colorama import init
import os
from datetime import timedelta

from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from werkzeug.security import generate_password_hash

from config import Config
from extensions import db, migrate, limiter, csrf, cors
from model.models import User
from helper import (
    upload_image,
    login_required,
    admin_required,
    load_users,
    check_password,
    cart_count,
)
from front import user_bp
from admin import admin_bp

# Application Initialization
app = Flask(__name__)
app.config.from_object(Config)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

db.init_app(app)
migrate.init_app(app, db)
limiter.init_app(app)
csrf.init_app(app)

# CORS Configuration for Angular frontend
cors.init_app(app)

# --- API Test Endpoint for CORS Testing ---
@app.route('/api/test', methods=['GET'])
def api_test():
    return {
        "status": "success",
        "message": "CORS is working! Angular connected successfully to Flask backend on port 9000."
    }


# Register Blueprints with URL Prefixes
app.register_blueprint(user_bp, url_prefix="")
app.register_blueprint(admin_bp, url_prefix="/admin")


# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"), 404


@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template("error/429.html"), 429


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error/500.html"), 500


# Context Processors
@app.context_processor
def inject_current_user():
    user = None
    user_id = session.get("user_id")
    user_email = session.get("user_email")
    if user_id:
        user = User.query.get(user_id)
    elif user_email:
        user = User.query.filter_by(email=user_email).first()

    if user:
        initials = "".join([part[0].upper() for part in (user.fullname or user.email).split()[:2]]) or "U"
        return {
            "current_user": {
                "id": user.id,
                "name": user.fullname or user.email.split("@")[0],
                "fullname": user.fullname or user.email.split("@")[0],
                "email": user.email,
                "image": user.image,
                "role": user.role,
                "status": user.status,
                "avatar": initials,
            }
        }

    return {
        "current_user": {
            "id": None,
            "name": session.get("username") or session.get("admin_name") or "Admin",
            "fullname": session.get("username") or session.get("admin_name") or "CHAY NITA",
            "email": session.get("user_email") or "admin@techey.tech",
            "image": session.get("user_image") or "/static/uploads/20260824153548_profile.jpg",
            "role": session.get("user_role") or "Super Admin",
            "status": "Active",
            "avatar": "CN",
        }
    }


@app.context_processor
def inject_globals():
    current_user = None
    user_email = session.get("user_email")

    if user_email:
        current_user = User.query.filter_by(email=user_email).first()
        if not current_user:
            current_user = load_users().get(user_email)

    return {"cart_count": cart_count(), "current_user": current_user}

if __name__ == "__main__":
    app.run(debug=True, port=5001)
