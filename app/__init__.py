import os
import time
import random
from flask_mail import Mail, Message

from flask import Flask, render_template, send_from_directory, request
from flask_login import LoginManager, login_required
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)
migrate = Migrate(app, db)
mail = Mail(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Будь ласка, увійдіть до системи для перегляду даної сторінки.'

from app.controllers import auth_controller, home_controller, manage_controller
from app.models import Device, Event, Home, LightingSettings, Log, Notification, Room, Schedule, Sensor, Users

from flask import jsonify

# Емуляція даних пристроїв освітлення та клімат-контролю
devices = {
    1: {'type': 'lighting', 'name': 'Лампочка', 'is_on': False, 'brightness': 0},
    2: {'type': 'climate', 'name': 'Кондиціонер', 'is_on': False, 'temperature': 20, 'humidity': 50},
}

# Маршрут для вмикання/вимикання пристроїв
@app.route('/api/device/<int:device_id>/toggle', methods=['POST', 'GET'])
def toggle_device(device_id):
    if device_id in devices:
        device = devices[device_id]
        device['is_on'] = not device['is_on']
        return jsonify({'success': True, 'is_on': device['is_on']})
    else:
        return jsonify({'success': False, 'message': 'Device not found'}), 404

# Маршрут для зміни яскравості освітлення
@app.route('/api/device/<int:device_id>/set_brightness', methods=['POST'])
def set_brightness(device_id):
    brightness = request.json.get('brightness')
    if brightness is not None:
        if device_id in devices and devices[device_id]['type'] == 'lighting':
            devices[device_id]['brightness'] = brightness
            return jsonify({'success': True, 'brightness': brightness})
        else:
            return jsonify({'success': False, 'message': 'Invalid device ID or type'}), 400
    else:
        return jsonify({'success': False, 'message': 'Brightness not provided'}), 400

# Маршрут для зміни температури клімат-контролю
@app.route('/api/device/<int:device_id>/set_temperature', methods=['POST'])
def set_temperature(device_id):
    temperature = request.json.get('temperature')
    if temperature is not None:
        if device_id in devices and devices[device_id]['type'] == 'climate':
            devices[device_id]['temperature'] = temperature
            return jsonify({'success': True, 'temperature': temperature})
        else:
            return jsonify({'success': False, 'message': 'Invalid device ID or type'}), 400
    else:
        return jsonify({'success': False, 'message': 'Temperature not provided'}), 400

# Емуляція випадкових значень пристроїв
def simulate_devices():
    while True:
        for device_id, device in devices.items():
            if device['type'] == 'lighting':
                device['is_on'] = random.choice([True, False])
                device['brightness'] = random.randint(0, 100)
            elif device['type'] == 'climate':
                device['is_on'] = random.choice([True, False])
                device['temperature'] += random.uniform(-1, 1)
                device['humidity'] += random.uniform(-1, 1)
        time.sleep(5)  # Оновлюємо значення кожні 5 секунд
#
# @app.route('/api/device/<int:device_id>/toggle', methods=['POST'])
# @login_required
# def toggle_device(device_id):
#     device = Device.query.get_or_404(device_id)
#     device.is_on = not device.is_on
#     db.session.commit()
#     return jsonify({'success': True, 'is_on': device.is_on})
#
# @app.route('/api/device/<int:device_id>/set_brightness', methods=['POST'])
# @login_required
# def set_brightness(device_id):
#     device = Device.query.get_or_404(device_id)
#     brightness = request.json.get('brightness')
#     if brightness is not None:
#         device.brightness = brightness
#         db.session.commit()
#         return jsonify({'success': True, 'brightness': device.brightness})
#     return jsonify({'success': False, 'message': 'Brightness not provided'}), 400
#
# @app.route('/api/device/<int:device_id>/set_temperature', methods=['POST'])
# @login_required
# def set_temperature(device_id):
#     device = Device.query.get_or_404(device_id)
#     temperature = request.json.get('temperature')
#     if temperature is not None:
#         device.set_temperature = temperature
#         db.session.commit()
#         return jsonify({'success': True, 'set_temperature': device.set_temperature})
#     return jsonify({'success': False, 'message': 'Temperature not provided'}), 400




# # Декоратор для перевірки аутентифікації
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'user_id' not in session:
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function


@login_manager.user_loader
def load_user(id):
    return Users.Users.query.get(int(id))


@app.route('/hibiscus.png')
def icon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'hibiscus.png', mimetype='image/png')
