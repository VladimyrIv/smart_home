from datetime import datetime
from app import db


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(200), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
