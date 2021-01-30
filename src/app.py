import os
from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UsersModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    pw_hash = db.Column(db.String(128))
    joined_at_datetime = db.Column(db.DateTime())

    def __init__(self, email, pw_hash, joined_at_datetime):
        self.email = email
        self.pw_hash = pw_hash
        self.joined_at_datetime = joined_at_datetime

    def __repr__(self):
        return f"<User {self.email}>"


@app.route("/")
def index():
    return jsonify({"hello": "world", "environment": os.environ["FLASK_ENV"]})


@app.route("/users", methods=["POST", "GET"])
def handle_users():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            new_user = UsersModel(
                email=data["email"],
                pw_hash=data["pw_hash"],
                joined_at_datetime=datetime.utcnow(),
            )
            db.session.add(new_user)
            db.session.commit()
            return {
                "message": f"user {new_user.email} has been created successfully."
            }, 201
        else:
            return {"error": "Invalid request"}, 400

    elif request.method == "GET":
        users = UsersModel.query.all()
        results = [
            {"email": user.email, "joined_at_datetime": user.joined_at_datetime}
            for user in users
        ]

        return {"count": len(results), "users": results}


if __name__ == "__main__":
    app.run()
