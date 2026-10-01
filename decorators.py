from functools import wraps
from flask import session, flash, redirect, url_for, request


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        # 1. Check if logged in
        if not session.get("user_id") and not session.get("admin_logged_in"):
            flash("Admin access required. Please log in first.", "warning")
            return redirect(url_for("admin.admin_login", next=request.path))

        # 2. Check admin role or flag
        role = session.get("user_role") or session.get("role")
        if role != "Admin" and not session.get("admin_logged_in"):
            flash("Access denied. Admin privileges required.", "danger")
            return redirect(url_for("admin.admin_login", next=request.path))

        return view(*args, **kwargs)

    return wrapped


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in first.", "warning")
            return redirect(url_for("user.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped