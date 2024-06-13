from app import db


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    schedules = db.relationship('Schedule', backref='device', lazy=True)
    events = db.relationship('Event', backref='device', lazy=True)
    logs = db.relationship('Log', backref='device', lazy=True)
    lighting_settings = db.relationship('LightingSettings', backref='device', lazy=True, uselist=False)
