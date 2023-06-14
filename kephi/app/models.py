from . import db
from datetime import datetime

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    subject = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.utcnow)

