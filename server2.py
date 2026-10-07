from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

# ===== НАСТРОЙКИ =====
TELEGRAM_TOKEN = "8572692875:AAHsx-38FyXqIVOl2yUmuzL3f2zfSq6tCi0"
TELEGRAM_CHAT_ID = "958909619"
# =====================

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    text = data.get('message', '').strip()

    if not text:
        return jsonify({'error': 'Пустое сообщение'}), 400

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"💌 Сообщение от Виолы:\n\n{text}",
        "parse_mode": "HTML"
    }

    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 200:
            return jsonify({'ok': True})
        else:
            return jsonify({'error': r.text}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)