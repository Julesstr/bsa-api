from flask import Flask
import os

app = Flask(__name__)

webhook_url = os.environ.get("WEBHOOK_URL")

@app.route('/', methods=["POST"])
def hello_world():
    return webhook_url
