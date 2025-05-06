# app.py
from flask import Flask
from flask_mail import Mail
from config import Config
from user_manage import signup, login
from life_Stuff import get_balance, purchase_life
from QUiz_log import take_quiz, earn_cash

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)

app.add_url_rule('/signup', 'signup', signup, methods=['POST'])
app.add_url_rule('/login', 'login', login, methods=['POST'])
app.add_url_rule('/get_balance', 'get_balance', get_balance, methods=['GET'])
app.add_url_rule('/purchase_life', 'purchase_life', purchase_life, methods=['POST'])
app.add_url_rule('/take_quiz', 'take_quiz', take_quiz, methods=['POST'])
app.add_url_rule('/earn_cash', 'earn_cash', earn_cash, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)