from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user') # admin, user

class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    department = db.Column(db.String(50))

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='draft') # draft, active, completed
    template_id = db.Column(db.Integer, db.ForeignKey('email_template.id'))
    
class EmailTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body_content = db.Column(db.Text, nullable=False) # HTML content
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_ai_generated = db.Column(db.Boolean, default=False)

class PhishingResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    target_id = db.Column(db.Integer, db.ForeignKey('target.id'))
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    opened = db.Column(db.Boolean, default=False)
    clicked_link = db.Column(db.Boolean, default=False)
    submitted_credentials = db.Column(db.Boolean, default=False)
    reported = db.Column(db.Boolean, default=False)
