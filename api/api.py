from mysql.connector import connect, Error
from flask import Flask, jsonify, request
from user import User

app = Flask(__name__)

DB_HOST = "192.168.1.100"
DB_USER = "ping_api"
DB_PASS = "pigga"

@app.route("/registeruser", methods=["POST"])
def register_user():
    try:
        with connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database="ping"
        ) as conn:
            user = User(
                username=request.form['username'],
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                password=request.form['password']
            )
            print(user)
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM users WHERE username = %s", (user.username,))
                if not cur.fetchmany(size=1):
                    query = "INSERT INTO users (username, first_name, last_name, password) VALUES (%s, %s, %s, %s);"
                    cur.execute(query, (user.username, user.first_name, user.last_name, user.password))
                    conn.commit()
                    print("User added")
                    query = "SELECT id FROM users WHERE username = %s"
                    cur.execute(query, (user.username,))
                    user_id = cur.fetchmany(size=1)
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
    except Error as e:
        print(f"database error: {e}")
        return jsonify({
            "error": {
                "code": 500,
                "message": "internal server error"
            }
        }), 500
    except KeyError as e:
        print(f"missing form field: {e}")
        return jsonify({
            "error": {
                "code": 400,
                "message": f"missing field: {str(e)}"
            }
        }), 400


@app.route("/loginuser", methods=["POST"])
def get_user():
    try:
        with connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database="ping"
        ) as conn:
            with conn.cursor as cur:
                query = "SELECT * FROM users WHERE username = %s AND password = %s;"
                cur.execute(query, (request.form['username'], request.form['password']))
                account = cur.fetchone()
                if account:
                    return jsonify({
                        'user_id': account['id']
                    })
                else:
                    return jsonify({
                        'error': {
                            'code': 404,
                            'message': 'Username or password incorrect'
                        }
                    })

    except Error as e:
        return jsonify({
            'error': {
                'code': 500,
                'message': "Internal server error"
            }
        })
