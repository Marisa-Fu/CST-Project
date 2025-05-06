from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
bcrypt = Bcrypt(app)

CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fightme_2005!",
        database="trivia_game"
    )

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({"error": "Username, password, and email are required"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)", (username, hashed_password, email))
        db.commit()
        return jsonify({"message": "Signup successful"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Username or email already taken"}), 400
    finally:
        cursor.close()
        db.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user and bcrypt.check_password_hash(user['password_hash'], password):
        return jsonify({
            "message": "Login successful",
            "user_id": user['user_id'],
            "cash": user['cash'],
            "lives": user['lives']
        }), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)