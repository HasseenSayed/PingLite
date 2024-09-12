from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def practice():
    return render_template("base.html", title="Nigga", thing="Aw hell nahh they took practice legs =(")