from flask import Flask, render_template, redirect, request, session
from werkzeug.middleware.proxy_fix import ProxyFix
import requests
import json
from models import User

app = Flask(__name__)
app.secret_key = "test"
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

@app.route("/")
def home():
    if 'loggedin' in session: 
        return render_template("home.html")
    return render_template("home.html", title="Nigga")

@app.route("/profile", methods=["GET"])
def profile():
    if 'loggedin' in session:
        # Create a user object from session data
        user_data = {
            'username': session.get('username'),
            'user_id': session.get('user_id', 0),
            'user_first_name': session.get('first_name', ''),
            'user_last_name': session.get('last_name', ''),
            'user_email': session.get('email', '')
        }
        user = User.from_dict(user_data)
        return render_template("profile.html", user=user.to_dict())
    else:
        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(request.get_data())
        res = requests.post("http://127.0.0.1:6000/loginuser", data=request.form.to_dict())
        print(res.status_code)
        if res.status_code == 404:
            print("Login failed")
            return render_template("login_error.html", content="Username/password error.")
        else:
            # If the API returns user data, store it in session
            try:
                response_data = res.json()
                if 'user_id' in response_data:
                    session['user_id'] = response_data.get('user_id')
                if 'user_first_name' in response_data:
                    session['first_name'] = response_data.get('user_first_name')
                if 'user_last_name' in response_data:
                    session['last_name'] = response_data.get('user_last_name')
                if 'user_email' in response_data:
                    session['email'] = response_data.get('user_email')
            except:
                pass  # If response is not JSON or doesn't contain user data, just continue
            
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
    return render_template("register.html", title="Register User")

@app.route("/user-already-exists")
def userexistserror():
    return render_template("user_exists.html", title="Error")

@app.route("/logout")
def logout():
    # Clear the session
    session.clear()
    return redirect("/")
