from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import mysql.connector

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Connect to your MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Fightme_2005!",  # CHANGE THIS TO YOUR MySQL password
    database="trivia_game"
)
cursor = db.cursor(dictionary=True)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
        db.commit()
        return jsonify({"message": "Signup successful"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Username already taken"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

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