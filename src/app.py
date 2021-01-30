from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"hello": "world", "environment": os.environ["FLASK_ENV"]})


if __name__ == "__main__":
    app.run()
