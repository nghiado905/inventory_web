from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ThuChi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thu = db.Column(db.Float, nullable=True)
    chi = db.Column(db.Float, nullable=True)
    reason = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date, default=datetime.now)

class HoaBinh(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=datetime.now)

class Deo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=datetime.now)
