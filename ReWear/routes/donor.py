from pathlib import Path
from uuid import uuid4
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from models import db, Donation
from routes.helpers import role_required

donor_bp = Blueprint("donor", __name__, url_prefix="/donor")


@donor_bp.route("/dashboard")
@login_required
@role_required("DONOR")
def dashboard():
    donations = Donation.query.filter_by(donor_id=current_user.id).order_by(Donation.created_at.desc()).all()
    return render_template("donor/dashboard.html", donations=donations, total=len(donations), available=sum(d.status == "AVAILABLE" for d in donations), claimed=sum(d.status == "CLAIMED" for d in donations))


@donor_bp.route("/donate", methods=["GET", "POST"])
@login_required
@role_required("DONOR")
def donate():
    if request.method == "POST":
        data = request.form
        required = ["title", "category", "description", "quantity", "condition", "pickup_address", "contact_number"]
        if not all(data.get(x, "").strip() for x in required) or not data.get("quantity", "").isdigit() or int(data["quantity"]) < 1:
            flash("Please complete all fields with a valid quantity.", "error"); return render_template("donor/donate.html")
        image_path = None; image = request.files.get("image")
        if image and image.filename:
            ext = Path(image.filename).suffix.lower().lstrip(".")
            if ext not in current_app.config["ALLOWED_EXTENSIONS"]:
                flash("Upload a PNG, JPG, JPEG, or WEBP image.", "error"); return render_template("donor/donate.html")
            filename = f"{uuid4().hex}_{secure_filename(image.filename)}"
            image.save(current_app.config["UPLOAD_FOLDER"] / filename); image_path = f"uploads/{filename}"
        db.session.add(Donation(donor_id=current_user.id, title=data["title"].strip(), category=data["category"], description=data["description"].strip(), quantity=int(data["quantity"]), condition=data["condition"], image_path=image_path, pickup_address=data["pickup_address"].strip(), contact_number=data["contact_number"].strip()))
        db.session.commit(); flash("Your donation is now available to NGOs.", "success")
        return redirect(url_for("donor.history"))
    return render_template("donor/donate.html")


@donor_bp.route("/history")
@login_required
@role_required("DONOR")
def history():
    return render_template("donor/history.html", donations=Donation.query.filter_by(donor_id=current_user.id).order_by(Donation.created_at.desc()).all())
