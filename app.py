pip install flask requests
python app.py
from flask import Flask, render_template, request, jsonify
import requests
import time
import random

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/spam", methods=["POST"])
def spam():
    ngl_link = request.form.get("link")
    message = request.form.get("message")
    count = int(request.form.get("count", 1))

    sent = 0
    errors = []

    for i in range(count):
        try:
            payload = {
                "question": message,
                "deviceId": ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=16))
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 Chrome/86.0.4240.198 Mobile Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            r = requests.post(f"{ngl_link}/message", data=payload, headers=headers, timeout=5)
            if r.status_code == 200:
                sent += 1
            else:
                errors.append(f"Error {r.status_code}")
            time.sleep(1)  # delay to avoid rate limiting
        except Exception as e:
            errors.append(str(e))
            break

    return jsonify({"sent": sent, "errors": errors})

if __name__ == "__main__":
    app.run(debug=True)
