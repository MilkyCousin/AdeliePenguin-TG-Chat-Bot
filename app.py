from flask import Flask, request
from flask_sslify import SSLify
from static.bot import AppManager
import json

app = Flask(__name__)
sslify = SSLify(app)

bot = AppManager()


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        response = request.get_json()
        bot.handle_message(response)
    return 'Hello Penguin!'


if __name__ == '__main__':
    app.run()
