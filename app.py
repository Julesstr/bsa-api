from flask import Flask, request
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import json


app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

webhook_url = os.environ.get("WEBHOOK_URL")
drip_user = os.environ.get("DRIP_USER")
drip_token = os.environ.get("DRIP_TOKEN")

@app.route(f"/webhook/{webhook_url}", methods=["POST"])
@limiter.limit("5 per minute")
def receive_webhook():
    data = request.get_json()
    url = f"https://api.getdrip.com/v3/{drip_user}/shopper_activity/order"
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Basic {drip_token}",
        "Access-Control-Allow-Origin": "*" 
    }

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
