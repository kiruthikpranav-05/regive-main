from flask import Blueprint, render_template, request
from flask_login import login_required
from models import Donation, User
from routes.helpers import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@login_required
@role_required("ADMIN")
def dashboard():
    return render_template("admin/dashboard.html", total_users=User.query.count(), donors=User.query.filter_by(role="DONOR").count(), ngos=User.query.filter_by(role="NGO").count(), total_donations=Donation.query.count(), available=Donation.query.filter_by(status="AVAILABLE").count(), claimed=Donation.query.filter_by(status="CLAIMED").count())


@admin_bp.route("/users")
@login_required
@role_required("ADMIN")
def users():
    query = User.query; search, role = request.args.get("search", "").strip(), request.args.get("role", "")
    if search: query = query.filter((User.name.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%")))
    if role in ("DONOR", "NGO", "ADMIN"): query = query.filter_by(role=role)
    return render_template("admin/users.html", users=query.order_by(User.created_at.desc()).all(), search=search, role=role)


@admin_bp.route("/donations")
@login_required
@role_required("ADMIN")
def donations():
    query = Donation.query; search, status, category = request.args.get("search", "").strip(), request.args.get("status", ""), request.args.get("category", "")
    if search: query = query.filter(Donation.title.ilike(f"%{search}%"))
    if status in ("AVAILABLE", "CLAIMED"): query = query.filter_by(status=status)
    if category: query = query.filter_by(category=category)
    return render_template("admin/donations.html", donations=query.order_by(Donation.created_at.desc()).all(), search=search, status=status, category=category)
