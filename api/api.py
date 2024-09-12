import sqlite3
from flask import Flask, jsonify
import user

app = Flask(__name__)



@app.route("/register", methods=["POST"])
def register_user():
    conn = sqlite3.connect("C:\\Users\\Hasseen Sayed\\Desktop\\PingLite\\database.db")
    cur = conn.cursor()
    query = "INSERT INTO users (username, first_name, last_name, password) VALUES ('Tester', 'John', 'Doe', 'password123');"
    res = cur.execute(query)
    conn.commit()


@app.route("/getuser/<username>")
def get_user(username):
    with sqlite3.connect("C:\\Users\\Hasseen Sayed\\Desktop\\PingLite\\database.db") as conn:
        cur = conn.cursor()
        query = "SELECT username, first_name, last_name, password FROM users where username like ?"
        res = cur.execute(query, (username, ))
        row = res.fetchone()
        usr = user.User(row[0], row[1], row[2], row[3])
        return usr.toJSON()