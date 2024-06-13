from app import db


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=False)
    devices = db.relationship('Device', backref='room', lazy=True)
    sensors = db.relationship('Sensor', backref='room', lazy=True)