from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail, Message
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

bcrypt = Bcrypt(app)
CORS(app)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pycodequiz@gmail.com' 
app.config['MAIL_PASSWORD'] = 'kdolnxgfzrutiomo'    
app.config['MAIL_DEFAULT_SENDER'] = 'pycodequiz@gmail.com'

mail = Mail(app)

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
        cursor.execute("INSERT INTO users (username, password_hash, email, cash, lives) VALUES (%s, %s, %s, 500, 0)", (username, hashed_password, email))
        db.commit()

        # Send confirmation email
        msg = Message('Welcome to Trivia Game!', recipients=[email])
        msg.body = f"Hi {username},\n\nThank you for signing up! You received $500 virtual currency to start playing.\n\nEnjoy!"
        mail.send(msg)

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
        session['user_id'] = user['user_id']
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
        return jsonify({'cash': balance['cash'], 'lives': balance['lives']})
    else:
        return jsonify({'error': 'User not logged in'}), 400

@app.route('/purchase_life', methods=['POST'])
def purchase_life():
    user_id = request.json.get('user_id')

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT cash, lives, email FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if user['cash'] >= 100:
            new_cash = user['cash'] - 100
            new_lives = user['lives'] + 1
            cursor.execute("UPDATE users SET cash = %s, lives = %s WHERE user_id = %s", (new_cash, new_lives, user_id))
            db.commit()

            # Send email confirmation
            msg = Message('Life Purchased', recipients=[user['email']])
            msg.body = "You successfully purchased a life for $100. Good luck on your next quiz!"
            mail.send(msg)

            return jsonify({"message": "Life purchased successfully"}), 200
        else:
            return jsonify({"error": "Not enough cash to purchase a life"}), 400
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/earn_cash', methods=['POST'])
def earn_cash():
    user_id = session.get('user_id')
    if user_id:
        score = request.json.get('score')
        level = request.json.get('level')
        reward = 0

        if level == 1:
            reward = 50 if score == 10 else 25 if score >= 6 else 0
        elif level == 2:
            reward = 100 if score == 10 else 50 if score >= 6 else 0
        elif level == 3:
            reward = 150 if score == 10 else 75 if score >= 6 else 0

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("UPDATE users SET cash = cash + %s WHERE user_id = %s", (reward, user_id))
        db.commit()
        cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)", (user_id, 'quiz_reward', reward))
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
        lives = cursor.fetchone()['lives']

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

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT username FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user:
        msg = Message('Password Reset Request', recipients=[email])
        msg.body = (
            f"Hi {user['username']},\n\nIf you forgot your password, please contact support or visit your profile to change it securely.\n\nThis is an automated message."
        )
        mail.send(msg)
        return jsonify({'message': 'Password reset email sent.'}), 200
    else:
        return jsonify({'error': 'Email not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

# test mail
@app.route('/check_username', methods=['POST'])
def check_username():
    data = request.json
    username = data.get('username')

    # Check if username already exists in the database
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user:
        return jsonify({"available": False})
    else:
        return jsonify({"available": True})
    
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Password validation (same regex from JS to double check)
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$"
    if not re.match(password_regex, password):
        return jsonify({"error": "Password must be at least 8 characters, contain at least one uppercase letter, one lowercase letter, and one special character."}), 400

    # Check if username already exists in the database
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        cursor.close()
        db.close()
        return jsonify({"error": "Username already taken"}), 400

    # Hash the password and insert new user into the database
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        cursor.execute("INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)", 
                       (username, hashed_password, email))
        db.commit()
        return jsonify({"message": "Signup successful"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error: {err}"}), 500
    finally:
        cursor.close()
        db.close()