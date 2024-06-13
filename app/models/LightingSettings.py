from app import db


class LightingSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    light_level = db.Column(db.Integer, nullable=False, default=0)  # Датчик освітленості
    motion_detected = db.Column(db.Boolean, nullable=False, default=False)  # Датчик руху
    presence_detected = db.Column(db.Boolean, nullable=False, default=False)  # Датчик присутності
    auto_on = db.Column(db.Boolean, nullable=False, default=False)
    auto_off = db.Column(db.Boolean, nullable=False, default=False)