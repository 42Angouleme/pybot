import sqlite3
from flask import Flask, Blueprint, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET KEY'] = 'secret'
app.secret_key = 'secret'

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return  connection
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/list')
def list_page():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM name').fetchall()
    connection.commit()
    connection.close()
    return render_template("list.html", posts=posts, image="placeholder")

@app.route('/result', methods=('GET', 'POST'))
def result_page():
    con = get_db_connection()
    truc = con.cursor()
    truc = con.execute("SELECT * FROM name where name LIKE ?", ("élève1", )).fetchone()
    con.close()
    return render_template("result.html", truc=truc)

@app.route('/search', methods=('GET', 'POST'))
def search_page():
    con = get_db_connection()
    res = con.execute('SELECT * FROM name').fetchall()
    con.commit()
    if request.method == 'POST':
        names = request.form['name']
        if names:
            res = con.execute("SELECT firstname FROM name WHERE name LIKE ?", (names, )).fetchall()
            con.commit()
            con.close()
            return redirect(url_for('result_page'))

    return render_template("search.html")

@app.route('/add', methods=('GET', 'POST'))
def add_page():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM name').fetchall()
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['firstname']
        image = ''
        if name and surname:
            posts = connection.execute('SELECT * FROM name').fetchall()
            connection.execute('INSERT INTO name(name, firstname) VALUES (?, ?)', (name, surname))
            connection.commit()
            connection.close()
            return render_template('name.html', name=name, surname=surname, image=image)

    return render_template("add.html", posts=posts)

@app.route('/record/<time>')
def record_audio(time):
    if (time.isdigit()):
        #relevant code for registering audio
        return ('recording...')
    return ('Invalid arguments')

@app.route('/<name>_<surname>')
def profile_page(name, surname):
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM name').fetchall()
    connection.commit()
    connection.close()
    return render_template("name.html", posts=posts, image="test.jpg", name=name, surname=surname)

@app.route('/<name>/delete', methods=('POST', 'DELETE'))
def delete_user(name):
    #delete user code
    return 'delete user'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8181)
