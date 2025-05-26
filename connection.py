import mysql.connector as sql
from dotenv import load_dotenv
import os

load_dotenv()

database = sql.connect(  # Connessione al database
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = database.cursor() #Creo il puntatore per il database, con uso solo per la LETTURA 

def commit():
    database.commit()

def get_cursor():
    return cursor

def is_connected():
    print(database.is_connected())