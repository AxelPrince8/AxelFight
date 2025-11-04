from flask import Flask, request, jsonify
import requests
import time
import threading

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "YOUR_FACEBOOK_PAGE_ACCESS_TOKEN"

def send_fb_message(recipient_id, message):
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    r = requests.post("https://graph.facebook.com/v11.0/me/messages",
                      params=params,
                      headers=headers,
                      json=data)
    return r.status_code == 200

def delayed_send(recipient_id, message, delay):
    time.sleep(delay)
    send_fb_message(recipient_id, message)

@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.get_json()
    recipient_id = data.get("recipientId")
    display_name = data.get("displayName")
    message_text = data.get("messageText")
    delay_seconds = data.get("delaySeconds", 10)

    full_message = f"{display_name}: {message_text}" if display_name else message_text

    # Run delayed send in background thread so server responds quickly
    thread = threading.Thread(target=delayed_send, args=(recipient_id, full_message, delay_seconds))
    thread.start()

    return jsonify({"message": "Message scheduled"}), 200

port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
