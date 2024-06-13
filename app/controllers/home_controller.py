from flask import render_template, session
from flask_login import login_required

from app import app
from app.models.Device import Device
from app.models.Home import Home
from app.models.Sensor import Sensor


@app.route('/')
@login_required
def index():
    user_id = session['user_id']
    homes = Home.query.filter_by(user_id=user_id).all()
    return render_template('index.html', homes=homes)