from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash

from extensions import db
from model.models import User
from helper import upload_image, get_admin_users_list
from decorators import admin_required
from . import admin_bp


@admin_bp.route("/users")
@admin_required
def admin_users():
    users_list = get_admin_users_list()
    return render_template("admin/user/index.html", active_page="user", users=users_list)


@admin_bp.route("/users/add", methods=["GET", "POST"])
@admin_required
def admin_user_add():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        role = request.form.get("role", "Customer")
        status = request.form.get("status", "Active")

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("User with this email already exists.", "warning")
            return redirect(url_for("admin.admin_user_add"))

        image_path = None
        if "image" in request.files:
            image_file = request.files["image"]
            if image_file and image_file.filename:
                image_path = upload_image(image_file)

        hashed_pwd = generate_password_hash(password) if password else generate_password_hash("default123")

        new_user = User(
            fullname=name,
            email=email,
            password=hashed_pwd,
            image=image_path,
            role=role,
            status=status,
        )
        db.session.add(new_user)
        db.session.commit()
        flash(f'User "{name}" created successfully!', "success")
        return redirect(url_for("admin.admin_users"))

    return render_template("admin/user/add.html", active_page="user")


@admin_bp.route("/users/edit/<int:user_id>", methods=["GET", "POST"])
@admin_required
def admin_user_edit(user_id):
    u = User.query.get(user_id)
    if not u:
        flash("User not found.", "danger")
        return redirect(url_for("admin.admin_users"))

    if request.method == "POST":
        u.fullname = request.form.get("name", u.fullname).strip()
        u.email = request.form.get("email", u.email).strip().lower()
        new_pwd = request.form.get("password", "").strip()
        if new_pwd:
            u.password = generate_password_hash(new_pwd)
        if "image" in request.files:
            image_file = request.files["image"]
            if image_file and image_file.filename:
                uploaded = upload_image(image_file)
                if uploaded:
                    u.image = uploaded
        u.role = request.form.get("role", u.role)
        u.status = request.form.get("status", u.status)
        db.session.commit()
        flash(f'User "{u.fullname}" updated successfully!', "success")
        return redirect(url_for("admin.admin_users"))

    user_dict = {
        "id": u.id,
        "name": u.fullname or u.email.split("@")[0],
        "email": u.email,
        "image": u.image,
        "role": u.role,
        "status": u.status,
    }
    return render_template("admin/user/edit.html", active_page="user", user=user_dict)


@admin_bp.post("/users/delete/<int:user_id>")
@admin_required
def admin_user_delete(user_id):
    u = User.query.get(user_id)
    if u:
        db.session.delete(u)
        db.session.commit()
        flash("User deleted successfully.", "info")
    return redirect(url_for("admin.admin_users"))
