from flask import Flask, redirect, url_for, render_template, request, session
import short_url as short
import login_database

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form.get("testo")
        print(long_url)
        try:
            result = short.create_url(long_url)
        except (ValueError, KeyError) as e:
            return render_template("index.html", errore=str(e))

        return render_template('index.html', short_url=result)

    return render_template("index.html")


@app.route(f'/<hex_url>')
def redirect_url(hex_url):
    url = short.get_things(hex_url, "hex_url", "url")
    short.click(hex_url)
    if url is None:
        return "URL non trovato", 404
    print(url[0])
    return redirect(url[0]) 

@app.route("/login", methods = ["GET", "POST"])
def login():
    answer = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        answer = login_database.password_check((username,password))

        print(username, password)
        print(answer)

    return render_template("login.html", answer = answer)
    
@app.route("/signup", methods = ["GET", "POST"])
def signup():
    answer = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        answer = login_database.add_user((username, password))

        print(username, password)
        print(answer)

    return render_template("signup.html", answer = answer )


if __name__ == '__main__':
    short.create_redirect_table()
    login_database.create_login_table()
    app.run(host='0.0.0.0', port = 5000, debug=True)