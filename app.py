from flask import Flask, request, jsonify
from db_connect import connect_db

app = Flask(__name__)

@app.route("/user/status", methods=["GET"])
def get_status():
    user_id = request.args.get("user_id")

    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT cash, lives FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    db.close()

    if result:
        return jsonify({"cash": result["cash"], "lives": result["lives"]})
    else:
        return jsonify({"error": "User not found"}), 404
    
    
@app.route("/user/buy_life", methods=["POST"])
def buy_life():
    user_id = request.json.get("user_id")

    db = connect_db()
    cursor = db.cursor()

    # Step 1: Check how much cash user has
    cursor.execute("SELECT cash FROM users WHERE user_id = %s", (user_id,))
    cash = cursor.fetchone()

    if cash and cash[0] >= 100:
        # Step 2: Deduct $100 and add 1 life
        cursor.execute("UPDATE users SET cash = cash - 100, lives = lives + 1 WHERE user_id = %s", (user_id,))
        
        # Step 3: Log the transaction
        cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (%s, 'life_purchase', 100)", (user_id,))
        
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"success": True, "message": "Life purchased!"})
    else:
        cursor.close()
        db.close()
        return jsonify({"success": False, "message": "Not enough cash."})