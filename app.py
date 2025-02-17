from flask import Flask, render_template, redirect, request, session
from werkzeug.middleware.proxy_fix import ProxyFix
import requests

app = Flask(__name__)
app.secret_key = "test"
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

user = None

@app.route("/")
def home():
    if 'loggedin' in session: 
        return render_template("home.html", loggedin=True)
    return render_template("home.html", title="Nigga")

@app.route("/profile", methods=["GET"])
def profile():
    if 'loggedin' in session:
        return render_template("profile.html")
    else:
        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(request.get_data())
        res = requests.post("http://127.0.0.1:6000/loginuser", data=request.form.to_dict())
        if res.status_code == 404:
            print("Login failed")
            return render_template("login_error.html", content="Username/password error.")
        else:
            session['loggedin'] = True
            return redirect("/")
    else:
        return render_template("login.html", title="Login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        res = requests.post("http://127.0.0.1:6000/registeruser", data=request.form.to_dict())
        if res.status_code == 409:
            print("Username already exists")
            return render_template("login_error.html", content="Username already exists blud.")

        return redirect("/")
    return render_template("register.html", title="Regiser User")

@app.route("/user-already-exists")
def userexistserror():
    return render_template("user_exists.html", title="Error")
