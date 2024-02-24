from flask import Flask
from sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

DATABASE = "./cows.sqlite3"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "cows.sqlite3"
)
db = SQLAlchemy(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


class Cow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    timestamp = db.Column(db.Integer(100), unique=False)
    battery_plugged = db.Column(db.Bolean, unique=False)
    battery_percent = db.Column(db.Integer, default=False, nullable=False)
    battery_remaining = db.Column(db.Boolean, default=False, nullable=False)
    user = db.Column(db.String(100), unique=False)
