from flask import Flask, render_template, redirect, request
import requests

app = Flask(__name__)

@app.route("/")
def practice():
    return render_template("base.html", title="Nigga", thing="Aw hell nahh they took practice legs =(")

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