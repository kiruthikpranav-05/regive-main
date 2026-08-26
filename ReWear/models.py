from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


def utcnow():
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    mobile = db.Column(db.String(25), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False, index=True)
    address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
    donations = db.relationship("Donation", foreign_keys="Donation.donor_id", back_populates="donor")
    claims = db.relationship("Donation", foreign_keys="Donation.claimed_by_ngo_id", back_populates="claimed_by")


class Donation(db.Model):
    __tablename__ = "donations"
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(140), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(30), nullable=False, index=True)
    image_path = db.Column(db.String(255), nullable=True)
    pickup_address = db.Column(db.Text, nullable=False)
    contact_number = db.Column(db.String(25), nullable=False)
    status = db.Column(db.String(15), nullable=False, default="AVAILABLE", index=True)
    claimed_by_ngo_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
    claimed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    donor = db.relationship("User", foreign_keys=[donor_id], back_populates="donations")
    claimed_by = db.relationship("User", foreign_keys=[claimed_by_ngo_id], back_populates="claims")
