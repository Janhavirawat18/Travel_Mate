from flask import Flask, render_template, request, url_for, redirect, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os
import googlemaps
import json
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
dotenv_path = find_dotenv()
if dotenv_path == "":
    raise FileNotFoundError(".env file not found")
else:
    print(f".env file found at: {dotenv_path}")

load_dotenv()

# Retrieve the API key
key = os.getenv("googleapikey")
if key is None:
    raise ValueError("The environment variable 'googleapikey' is not set.")

print(f"Google API Key: {key}")

app = Flask(__name__)
seckey = os.urandom(12)
app.secret_key = seckey
app.permanent_session_lifetime = timedelta(minutes=30)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
gmaps = googlemaps.Client(key=key)


class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    preferences = db.Column(db.String(1000), default="")  # places saved

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    def get_preferences(self):
        return [str(x) for x in self.preferences.split(";")]

    def set_preferences(self, val):
        self.preferences += ";" + str(val)


@app.route("/login", methods=["POST", "GET"])
def login():
    if "login" in session and session["login"]:
        return redirect(url_for("generic"))
    if request.method == "POST":
        q = Users.query.filter_by(email=request.form["email"]).first()
        if q and q.password == request.form["password"]:
            session["login"] = True
            session["name"] = q.name
            session["email"] = q.email
            app.permanent = True
            return redirect(url_for("generic"))
        return redirect(url_for("login"))
    else:
        return render_template("form.html")


@app.route("/logout")
def logout():
    session.clear()
    print(session)
    return redirect(url_for("mainpage"))


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"]
        found_user = Users.query.filter_by(email=email).first()
        if not found_user:
            usr = Users(email, name, password)
            db.session.add(usr)
            db.session.commit()
            session["login"] = True
            session["name"] = name
            session["email"] = email
            return redirect(url_for("login"))
        return redirect(url_for("register"))
    else:
        return render_template("register.html")


@app.route("/")
def mainpage():
    return render_template("index.html")


@app.route("/allusers")
def use():
    m = Users.query.all()
    x = ""
    for user in m:
        x += f"Test:"
        x += f"<p>{user.email}</p>"
        x += f"<p>{user.name}</p>"
        x += f"<p>{user.password}</p>"
        x += f"<p>{user.get_preferences()}</p>"
    return x


@app.route("/generic", methods=["POST", "GET"])
def generic():
    if "login" not in session or not session["login"]:
        return redirect(url_for("login"))
    name = "dude"
    if "curr" in session:
        listplc = session["curr"]
    else:
        listplc = []
    if "name" in session:
        name = session["name"]
    if request.method == "POST":
        for i in range(20):
            if str(i) in request.form:
                user = Users.query.filter_by(email=session["email"]).first()
                user.set_preferences(request.form[str(i)])
                db.session.commit()
        if "location" in request.form and "placetype" in request.form:
            location = request.form["location"]
            placetype = request.form["placetype"]
            loc = tuple(gmaps.geocode(address=location)[0]["geometry"]["location"].values())
            plac = gmaps.places(query="", location=loc, language="en", type=placetype)
            listplc = []
            for i in plac["results"]:
                if "photos" in i and "formatted_address" in i and "name" in i:
                    listplc.append({
                        "name": i["name"],
                        "address": i["formatted_address"],
                        "photo": "https://maps.googleapis.com/maps/api/place/photo?maxheight=385&maxwidth=300&photoreference=" + i["photos"][0]["photo_reference"] + "&key=" + key
                    })
            session["curr"] = listplc
            return render_template("generic.html", name=name, loop=True, places=listplc)
        return render_template("generic.html", name=name, loop=True, places=listplc)
    return render_template("generic.html", name=name, loop=False, places=listplc)


@app.route("/liked")
def liked():
    if "login" not in session or not session["login"]:
        return redirect(url_for("login"))
    user = Users.query.filter_by(email=session["email"]).first()
    lst = user.get_preferences()[1:]
    rtls = []
    for i in lst:
        print(type(i))
        rtls.append(json.loads(i.replace("'", "\"")))
    print(rtls)
    return render_template("liked.html", places=rtls)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
