from flask import Flask, request
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import json
import jsonify

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

sendowl_webhook_url = os.environ.get("SENDOWL_WEBHOOK_URL")
drip_user = os.environ.get("DRIP_USER")
drip_token = os.environ.get("DRIP_TOKEN")

calendly_webhook_url = os.environ.get("CALENDLY_WEBHOOK_URL")

url = f"https://api.getdrip.com/v3/{drip_user}/shopper_activity/order"
headers = {
    "Content-Type": "application/json",
    "authorization": f"Basic {drip_token}",
    "Access-Control-Allow-Origin": "*" 
}
    

@app.route(f"/sendowlcompleted/{sendowl_webhook_url}", methods=["POST"])
@limiter.limit("5 per minute")
def receive_sendowl_order_completed():
    data = request.get_json()

    payload = {
        "provider": "sendowl",
        "email": str(data["order"]["buyer_email"]),
        "action": "placed",
        "order_id": str(data["order"]["id"]),
        "grand_total": float(data["order"]["settled_gross"]),
        "items": [{"name": data["order"]["cart"]["cart_items"][0]["product"]["name"]}]

    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    return str(response.status_code), response.status_code


@app.route(f"/sendowlchargeback/{sendowl_webhook_url}", methods=["POST"])
@limiter.limit("5 per minute")
def receive_sendowl_order_completed():
    data = request.get_json()

    return jsonify(data)


@app.route(f"/calendlywebhook/{calendly_webhook_url}", methods=["POST"])
@limiter.limit("5 per minute")
def receive_calendly_webhook():
    data = request.get_json()

    try:
        payload = {
            "provider": "calendly",
            "email": data["payload"]["email"],
            "action": "placed",
            "order_id": data["payload"]["payment"]["external_id"],
            "grand_total": data["payload"]["payment"]["amount"],
            "items": [{"name": "One-on-One"}]

        }

    except TypeError:
        return "Free event"
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    return str(response.status_code), response.status_code