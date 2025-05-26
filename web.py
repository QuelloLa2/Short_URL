from flask import Flask, redirect, url_for, render_template, request, session
import initialize as database

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form.get("testo")
        print(long_url)
        try:
            result = database.create_url(long_url)
        except (ValueError, KeyError) as e:
            return render_template("index.html", errore=str(e))

        return render_template('index.html', short_url=result)

    return render_template("index.html")


@app.route(f'/<hex_url>')
def redirect_url(hex_url):
    url = database.get_things(hex_url, "hex_url", "url")
    database.click(hex_url)
    if url is None:
        return "URL non trovato", 404
    print(url[0])
    return redirect(url[0]) 


if __name__ == '__main__':
    database.create_redirect_table()
    app.run(host='0.0.0.0', port = 5000, debug=True)
    
