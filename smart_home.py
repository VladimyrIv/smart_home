from app import app, simulate_devices

if __name__ == "__main__":
    import threading

    threading.Thread(target=simulate_devices).start()
    app.run(debug=True, port = 5177)
