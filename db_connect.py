import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",             
        password="Fightme_2005!", 
        database="trivia_game"
    )
