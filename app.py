# from flask import Flask, jsonify, request
#
# app = Flask(__name__)
#
# led_status = "OFF"
#
# @app.route('/')
# def index():
#     return '''
#         <h1>Control LED</h1>
#         <button onclick="fetch('/led/on')">Turn ON</button>
#         <button onclick="fetch('/led/off')">Turn OFF</button>
#     '''
#
# @app.route('/led/<state>', methods=['GET'])
# def control_led(state):
#     global led_status
#     if state == "on":
#         led_status = "ON"
#     elif state == "off":
#         led_status = "OFF"
#     return ('', 204)
#
# @app.route('/led-status', methods=['GET'])
# def led_status_route():
#     return jsonify(led_status)
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


from flask import Flask, request

app = Flask(__name__)

@app.route('/led-status', methods=['GET'])
def led_status():
    return "LED status response"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Замените порт на используемый вами

dism /online /Enable-Feature /FeatureName:TelnetClient
