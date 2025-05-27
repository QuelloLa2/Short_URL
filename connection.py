import mysql.connector as sql
from dotenv import load_dotenv
import os

load_dotenv()

database = sql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_SHORT")
)

cursor = database.cursor()

def commit():
    database.commit()

def get_cursor():
    return cursor

def is_connected():
    print(database.is_connected())