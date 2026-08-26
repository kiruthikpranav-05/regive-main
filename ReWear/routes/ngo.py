from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import update
from models import db, Donation, utcnow
from routes.helpers import role_required

ngo_bp = Blueprint("ngo", __name__, url_prefix="/ngo")


@ngo_bp.route("/dashboard")
@login_required
@role_required("NGO")
def dashboard():
    query = Donation.query.filter_by(status="AVAILABLE")
    search, category, condition = request.args.get("search", "").strip(), request.args.get("category", ""), request.args.get("condition", "")
    if search: query = query.filter(Donation.title.ilike(f"%{search}%"))
    if category: query = query.filter_by(category=category)
    if condition: query = query.filter_by(condition=condition)
    donations = query.order_by(Donation.created_at.desc()).all()
    claims = Donation.query.filter_by(claimed_by_ngo_id=current_user.id).order_by(Donation.claimed_at.desc()).all()
    return render_template("ngo/dashboard.html", donations=donations, claims=claims, available_count=Donation.query.filter_by(status="AVAILABLE").count(), search=search, category=category, condition=condition)


@ngo_bp.route("/donation/<int:donation_id>")
@login_required
@role_required("NGO")
def donation_details(donation_id):
    donation = db.session.get(Donation, donation_id)
    if not donation: abort(404)
    if donation.status != "AVAILABLE":
        flash("This donation is no longer available.", "error"); return redirect(url_for("ngo.dashboard"))
    return render_template("ngo/donation_details.html", donation=donation)


@ngo_bp.route("/claim/<int:donation_id>", methods=["POST"])
@login_required
@role_required("NGO")
def claim(donation_id):
    # Conditional UPDATE is atomic: exactly one simultaneous requester can change AVAILABLE.
    result = db.session.execute(update(Donation).where(Donation.id == donation_id, Donation.status == "AVAILABLE").values(status="CLAIMED", claimed_by_ngo_id=current_user.id, claimed_at=utcnow()))
    if result.rowcount != 1:
        db.session.rollback(); flash("This donation has already been claimed by another NGO.", "error")
        return redirect(url_for("ngo.dashboard"))
    db.session.commit(); flash("Donation claimed successfully. Contact details are now in your history.", "success")
    return redirect(url_for("ngo.history"))


@ngo_bp.route("/history")
@login_required
@role_required("NGO")
def history():
    donations = Donation.query.filter_by(claimed_by_ngo_id=current_user.id).order_by(Donation.claimed_at.desc()).all()
    return render_template("ngo/history.html", donations=donations)
