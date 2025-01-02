from flask import Flask, render_template, redirect, request
from werkzeug.middleware.proxy_fix import ProxyFix
import requests

app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

@app.route("/")
def home():
    return render_template("home.html", title="Nigga")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        res = requests.post("http://127.0.0.1:6000/registeruser", data=request.form.to_dict())
        if res.status_code == 409:
            print("Username already exists")
            return redirect("/user-already-exists")

        return redirect("/")
    return render_template("register.html", title="Regiser User")

@app.route("/user-already-exists")
def userexistserror():
    return render_template("user_exists.html", title="Error")
