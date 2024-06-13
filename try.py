from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ESP32_IP = "https://wokwi.com/projects/320964045035274834"  # Укажите IP-адрес вашего ESP32

@app.route('/')
def index():
    return "ESP32 Control Server"

@app.route('/send_command', methods=['POST'])
def send_command():
    data = request.json
    command = data.get('command')
    response = requests.post(f"{ESP32_IP}/command", json={'command': command})
    return jsonify(response.json())

@app.route('/get_data', methods=['GET'])
def get_data():
    response = requests.get(f"{ESP32_IP}/data")
    print(response)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
