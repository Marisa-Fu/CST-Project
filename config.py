# config.py
import os

class Config:
    SECRET_KEY = 'your_secret_key_here'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'pycodequiz@gmail.com'
    MAIL_PASSWORD = 'kdolnxgfzrutiomo'
    MAIL_DEFAULT_SENDER = 'pycodequiz@gmail.com'
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = "Fightme_2005!"
    DB_NAME = "trivia_game"