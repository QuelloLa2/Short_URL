import connection
import os


default_url = "http://localhost:5000"
table = "redirect_table"
cursor = connection.get_cursor()

def create_redirect_table():
    cursor.execute(f''' CREATE TABLE IF NOT EXISTS {table} (
        url VARCHAR(255) NOT NULL UNIQUE,
        hex_url VARCHAR(255) NOT NULL UNIQUE,
        click INT NOT NULL 
    )
    ''')


def create_url(long_url):

    if control_protocol(long_url):
        print("Protocollo Sbagliato")
        raise ValueError("http:// o https:// non aggiunti")

    if control_duplicate(long_url):
        print("URL Duplicato")
        raise KeyError("URL duplicato")

    url = control("url", long_url)

    if url is not None: # contrllo url inserito
        return url

    create_hex_url = os.urandom(3).hex()
    temp_url = control("hex_url", create_hex_url)
    while temp_url is not None:
        create_hex_url = os.urandom(3).hex()
        temp_url = control("hex_url", create_hex_url)
    
    comand = f"INSERT IGNORE INTO {table} (url, hex_url, click) VALUES (%s,%s,%s)"
    cursor.execute(comand, (long_url, create_hex_url, 0 ))
    connection.commit()

    return default_url + "/" + create_hex_url


def get_things(hex_url, type, value):
    comand = f'SELECT {value} FROM {table} WHERE {type} = %s'
    cursor.execute(comand, (hex_url,))
    url = cursor.fetchone()
    if url is None:
        return None 
    return url

def control(type, url):
    comand = f"SELECT * FROM {table} WHERE {type} = %s"
    cursor.execute(comand, (url,) )
    result = cursor.fetchone()
    if result is not None:
        return f'{default_url}' + '/' + f'{result[1]}' 
    else:
        return None

def control_protocol(long_url):
    return not long_url.startswith(("https://", "http://"))


def control_duplicate(long_url):
    return long_url.startswith(default_url)

def get_all_url():
    comand = f"SELECT * FROM {table}"
    cursor.execute(comand)
    urls = cursor.fetchall()
    for url in urls:
        print(url)

def click(hex_url):
    comand = f"UPDATE {table} SET click = click + 1 WHERE hex_url = %s"
    cursor.execute(comand, (hex_url,))
    connection.commit()
    print(get_things(hex_url, "hex_url", "click")[0])
