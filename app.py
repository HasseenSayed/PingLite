from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route("/")
def practice():
    return render_template("base.html", title="Nigga", thing="Aw hell nahh they took practice legs =(")

@app.route("/register", method=["GET", "POST"])
def register_user():
    if request.method == "POST":
        pass