from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated: return redirect(url_for("auth.redirect_dashboard"))
    if request.method == "POST":
        role = request.form.get("role", "DONOR")
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        mobile = request.form.get("mobile", "").strip()
        address = request.form.get("address", "").strip()
        password, confirm = request.form.get("password", ""), request.form.get("confirm_password", "")
        if role not in ("DONOR", "NGO") or not all([name, email, mobile, password]):
            flash("Please complete all required fields.", "error")
        elif role == "NGO" and not address:
            flash("NGOs must provide an address.", "error")
        elif password != confirm or len(password) < 8:
            flash("Passwords must match and be at least 8 characters.", "error")
        elif User.query.filter_by(email=email).first():
            flash("That email address is already registered.", "error")
        else:
            db.session.add(User(name=name, email=email, mobile=mobile, address=address or None, role=role, password_hash=generate_password_hash(password)))
            db.session.commit(); flash("Account created. Please log in.", "success")
            return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated: return redirect(url_for("auth.redirect_dashboard"))
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email", "").strip().lower()).first()
        if user and check_password_hash(user.password_hash, request.form.get("password", "")):
            login_user(user); return redirect(url_for("auth.redirect_dashboard"))
        flash("Invalid email or password.", "error")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    logout_user(); flash("You have been logged out.", "success")
    return redirect(url_for("index"))


@auth_bp.route("/dashboard")
def redirect_dashboard():
    if not current_user.is_authenticated: return redirect(url_for("auth.login"))
    endpoints = {"DONOR": "donor.dashboard", "NGO": "ngo.dashboard", "ADMIN": "admin.dashboard"}
    return redirect(url_for(endpoints[current_user.role]))
