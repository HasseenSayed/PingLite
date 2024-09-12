import sqlite3
from flask import Flask
import user

app = Flask(__name__)

conn = sqlite3.connect("C:\\Users\\Hasseen Sayed\\Desktop\\PingLite\\database.db")
cur = conn.cursor()
query = "INSERT INTO users (username, first_name, last_name, password) VALUES ('Tester', 'John', 'Doe', 'password123');"
res = cur.execute(query)
conn.commit()


@app.route("/register", methods=["POST"])
def register_user():
    pass

@app.route("/getuser")
def get_user():
    pass