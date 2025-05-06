from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Secret key for session handling
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
        session['user_id'] = user['user_id']  # Save user_id to session
        return jsonify({
            "message": "Login successful",
            "user_id": user['user_id'],
            "cash": user['cash'],
            "lives": user['lives']
        }), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route('/get_balance', methods=['GET'])
def get_balance():
    user_id = session.get('user_id')
    if user_id:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT cash, lives FROM users WHERE user_id = %s", (user_id,))
        balance = cursor.fetchone()
        cursor.close()
        db.close()
        return jsonify({'cash': balance[0], 'lives': balance[1]})
    else:
        return jsonify({'error': 'User not logged in'}), 400

@app.route('/purchase_life', methods=['POST'])
def purchase_life():
    user_id = session.get('user_id')
    if user_id:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT cash FROM users WHERE user_id = %s", (user_id,))
        current_cash = cursor.fetchone()[0]

        if current_cash >= 100:  # Assuming lives cost $100
            cursor.execute("UPDATE users SET cash = cash - 100, lives = lives + 1 WHERE user_id = %s", (user_id,))
            db.commit()

            # Record the transaction
            cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)", (user_id, 'life_purchase', 100))
            db.commit()

            cursor.close()
            db.close()
            return jsonify({'message': 'Life purchased successfully'})
        else:
            cursor.close()
            db.close()
            return jsonify({'error': 'Not enough cash'}), 400
    else:
        return jsonify({'error': 'User not logged in'}), 400

@app.route('/earn_cash', methods=['POST'])
def earn_cash():
    user_id = session.get('user_id')
    if user_id:
        score = request.json.get('score')
        level = request.json.get('level')
        reward = 0

        if level == 1:
            if score == 10:
                reward = 50
            elif score >= 6:
                reward = 25
        elif level == 2:
            if score == 10:
                reward = 100
            elif score >= 6:
                reward = 50
        elif level == 3:
            if score == 10:
                reward = 150
            elif score >= 6:
                reward = 75

        # Update user's cash
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("UPDATE users SET cash = cash + %s WHERE user_id = %s", (reward, user_id))
        db.commit()

        # Record the transaction
        cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)",
                       (user_id, 'quiz_reward', reward))
        db.commit()

        cursor.close()
        db.close()
        return jsonify({'message': f'You earned {reward} cash!'})

    return jsonify({'error': 'User not logged in'}), 400

@app.route('/take_quiz', methods=['POST'])
def take_quiz():
    user_id = session.get('user_id')
    if user_id:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT lives FROM users WHERE user_id = %s", (user_id,))
        lives = cursor.fetchone()[0]

        if lives > 0:
            cursor.execute("UPDATE users SET lives = lives - 1 WHERE user_id = %s", (user_id,))
            db.commit()
            cursor.close()
            db.close()
            return jsonify({'message': 'Quiz started!'})
        else:
            cursor.close()
            db.close()
            return jsonify({'error': 'Not enough lives'}), 400
    else:
        return jsonify({'error': 'User not logged in'}), 400

if __name__ == '__main__':
    app.run(debug=True)
