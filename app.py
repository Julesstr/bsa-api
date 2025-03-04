from flask import Flask
import os

app = Flask(__name__)

webhook_url = os.environ.get("WEBHOOK_URL")
drip_user = os.environ.get("DRIP_USER")
drip_token = os.environ.get("DRIP_token")

@app.route(f"/webhook/{webhook_url}", methods=["POST"])
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

    return response.status_code
