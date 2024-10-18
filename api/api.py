import sqlite3
from flask import Flask, jsonify, request
from user import User

app = Flask(__name__)



@app.route("/registeruser", methods=["POST"])
def register_user():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    user = User(
        username=request.form['username'],
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        password=request.form['password']
    )
    print(user)
    res = cur.execute("SELECT id FROM users WHERE username = ?", (user.username, ))
    if not res.fetchone():
        query = "INSERT INTO users (username, first_name, last_name, password) VALUES (?, ?, ?, ?);"
        res = cur.execute(query, (user.username, user.first_name, user.last_name, user.password))
        conn.commit()
        print("User added")
        query = "SELECT id FROM users WHERE username = ?"
        res = cur.execute(query, (user.username, ))
        conn.commit()
        user_id = res.fetchone()
        return jsonify({
            'data': {
                'user_id': user_id
            }
        }), 200
    else:
        return jsonify({
            "error": {
                'code': 409,
                'message': "username already exists"
                }
            }), 409


@app.route("/getuser/<username>")
def get_user(username):
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        query = "SELECT username, first_name, last_name, password FROM users where username like ?"
        res = cur.execute(query, (username, ))
        row = res.fetchone()
        user = user.User(row[0], row[1], row[2], row[3])
        return user.toJSON()