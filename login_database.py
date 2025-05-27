import connection
import hashlib
from hmac import compare_digest
import os

name = "login_table"
cursor = connection.get_cursor()
r_salt = os.urandom(16).hex()

def create_login_table():
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {name} (
        user VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(512) NOT NULL,
        salt VARCHAR(512) NOT NULL
    )''')

def add_user(username):
    user, password = username
    salt = r_salt
    password = crypt_password(password, salt)
    comand = f"SELECT user FROM {name} WHERE user = %s"
    cursor.execute(comand, (user,))
    exist_user = cursor.fetchone()
    if exist_user is not None:
        return "Utente esistente"
    comand = f"INSERT IGNORE INTO {name} (user, password, salt) VALUES (%s, %s ,%s)"
    cursor.execute(comand, (user, password, salt))
    connection.commit()
    return "Utente aggiunto"

def get_password(user):
    comand = f"SELECT password, salt FROM {name} WHERE user = %s"
    cursor.execute(comand, (user,))
    pack = cursor.fetchone()
    return pack

def password_check(username):
    user, login_password = username
    pack = get_password(user)
    if pack is None:
        return "Utente non trovato"
        return
    hash_password, salt = pack
    login_password = crypt_password(login_password, salt)
    if compare_digest(hash_password, login_password):
        return True
    else:
        return "Password Errata"

def crypt_password(password,salt):
    hash_password = (hashlib.pbkdf2_hmac('sha256',password.encode(), salt.encode(), 10000)).hex()
    return hash_password

    