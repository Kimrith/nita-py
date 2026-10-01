from flask import render_template
from decorators import admin_required
from . import admin_bp


@admin_bp.route("/dashboard")
@admin_required
def admin_dashboard():
    return render_template("admin/dashboard/index.html", active_page="dashboard")