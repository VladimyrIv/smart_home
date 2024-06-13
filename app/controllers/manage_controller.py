from datetime import datetime
from mailbox import Message

from flask_login import login_required

from app import app, db, mail
from app.models.Device import Device
from flask import render_template, redirect, url_for, flash, request, session, jsonify

from app.models.Home import Home
from app.models.Log import Log
from app.models.Room import Room
from app.models.LightingSettings import LightingSettings
from app.models.Users import Users


def send_alert_email(user_email, message):
    msg = Message('Аварійне повідомлення з вашого розумного дому',
                  sender='your_email@example.com',
                  recipients=[user_email])
    msg.body = message
    mail.send(msg)


@app.route('/sensor_alert', methods=['POST'])
def sensor_alert():
    data = request.get_json()
    device_id = data['device_id']
    alert_type = data['alert_type']

    device = Device.query.get(device_id)
    user = Users.query.get(device.user_id)

    if alert_type in ['gas', 'fire']:
        alert_message = f"Увага! Спрацював датчик {alert_type} у пристрої {device.name}!"
        send_alert_email(user.email, alert_message)

    # Запис у лог
    new_log = Log(timestamp=datetime.utcnow(),
                  description=alert_message,
                  device_id=device.id,
                  user_id=user.id)
    db.session.add(new_log)
    db.session.commit()

    return jsonify({'message': 'Alert processed successfully'}), 200


@app.route('/add_log', methods=['POST'])
def add_log():
    data = request.get_json()
    new_log = Log(timestamp=datetime.utcnow(),
                  description=data['description'],
                  device_id=data['device_id'],
                  user_id=data['user_id'])
    db.session.add(new_log)
    db.session.commit()
    return jsonify({'message': 'Log added successfully'}), 201


@app.route('/add_home', methods=['GET', 'POST'])
@login_required
def add_home():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        user_id = session['user_id']
        new_home = Home(name=name, address=address, user_id=user_id)
        db.session.add(new_home)
        db.session.commit()
        flash('Будинок успішно додано!')
        return redirect(url_for('index'))
    return render_template('add_home.html')



@app.route('/edit_home/<int:home_id>', methods=['GET', 'POST'])
@login_required
def edit_home(home_id):
    home = Home.query.get_or_404(home_id)
    if request.method == 'POST':
        home.name = request.form['name']
        home.address = request.form['address']
        db.session.commit()
        flash('Дані будинку успішно оновлено!')
        return redirect(url_for('index'))
    return render_template('edit_home.html', home=home)

@app.route('/delete_home/<int:home_id>', methods=['POST'])
@login_required
def delete_home(home_id):
    home = Home.query.get_or_404(home_id)
    rooms = Room.query.filter_by(home_id=home.id).all()
    for room in rooms:
        devices = Device.query.filter_by(room_id=room.id).all()
        for device in devices:
            LightingSettings.query.filter_by(device_id=device.id).delete()
            db.session.delete(device)
        db.session.delete(room)
    db.session.delete(home)
    db.session.commit()
    flash('Будинок і всі пов\'язані з ним дані успішно видалені!')
    return redirect(url_for('index'))

@app.route('/home/<int:home_id>')
@login_required
def home_details(home_id):
    home = Home.query.get_or_404(home_id)
    rooms = Room.query.filter_by(home_id=home.id).all()
    return render_template('home_details.html', home=home, rooms=rooms)


@app.route('/home/<int:home_id>/devices')
@login_required
def home_devices(home_id):
    home = Home.query.get_or_404(home_id)
    rooms = Room.query.filter_by(home_id=home_id).all()

    lighting_devices = []
    climate_devices = []

    for room in rooms:
        lighting_devices.extend(Device.query.filter_by(room_id=room.id, type='lighting').all())
        climate_devices.extend(Device.query.filter_by(room_id=room.id, type='climate').all())

    return render_template('home_devices.html', home=home, lighting_devices=lighting_devices,
                           climate_devices=climate_devices)


@app.route('/add_room', methods=['GET', 'POST'])
@login_required
def add_room():
    user_id = session['user_id']
    homes = Home.query.filter_by(user_id=user_id).all()
    if request.method == 'POST':
        name = request.form['name']
        home_id = request.form['home_id']
        new_room = Room(name=name, home_id=home_id)
        db.session.add(new_room)
        db.session.commit()
        flash('Кімната успішно додана!')
        return redirect(url_for('home_details', home_id=home_id))
    return render_template('add_room.html', homes=homes)


@app.route('/room/<int:room_id>')
@login_required
def room_details(room_id):
    room = Room.query.get_or_404(room_id)
    lighting_devices = Device.query.filter_by(room_id=room_id, type='lighting').all()
    climate_devices = Device.query.filter_by(room_id=room_id, type='climate').all()
    return render_template('room_details.html', room=room, lighting_devices=lighting_devices, climate_devices=climate_devices)




@app.route('/add_device/<int:room_id>/<device_type>', methods=['GET', 'POST'])
@login_required
def add_device(room_id, device_type):
    if request.method == 'POST':
        name = request.form['name']
        new_device = Device(name=name, room_id=room_id, status="off", type=device_type)
        db.session.add(new_device)
        db.session.commit()
        flash(f'{device_type.capitalize()} пристрій успішно додано!')
        return redirect(url_for('room_details', room_id=room_id))
    return render_template('add_device.html', room_id=room_id, device_type=device_type)



@app.route('/lighting')
@login_required
def lighting():
    user_id = session['user_id']
    rooms = Room.query.join(Device).join(Home).filter(Home.user_id == user_id, Device.type == 'light').all()
    return render_template('lighting.html', rooms=rooms)


@app.route('/lighting/<int:room_id>')
@login_required
def lighting_room(room_id):
    room = Room.query.get_or_404(room_id)
    devices = Device.query.filter_by(room_id=room.id, type='light').all()
    return render_template('lighting_room.html', room=room, devices=devices)


@app.route('/lighting/settings/<int:device_id>', methods=['GET', 'POST'])
@login_required
def lighting_settings(device_id):
    device = Device.query.get_or_404(device_id)
    settings = LightingSettings.query.filter_by(device_id=device.id).first()
    if request.method == 'POST':
        settings.light_level = request.form['light_level']
        settings.motion_detected = 'motion_detected' in request.form
        settings.presence_detected = 'presence_detected' in request.form
        settings.auto_on = 'auto_on' in request.form
        settings.auto_off = 'auto_off' in request.form
        db.session.commit()
        return redirect(url_for('lighting_room', room_id=device.room_id))
    return render_template('lighting_settings.html', device=device, settings=settings)
