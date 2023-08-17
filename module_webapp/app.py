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

@app.route('/search')
def search_page():
    return render_template("search.html")

@app.route('/list')
def list_page():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM name').fetchall()
    connection.commit()
    connection.close()
    return render_template("list.html", posts=posts, image="placeholder")

@app.route('/add', methods=('GET', 'POST'))
def add_page():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM name').fetchall()
    connection.commit()
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

@app.route('/<name>')
def profile_page(name):
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM name').fetchall()
    connection.commit()
    connection.close()
    return render_template("name.html", posts=posts, image="test.jpg", name=name)

@app.route('/<name>/delete', methods=('POST', 'DELETE'))
def delete_user(name):
    #delete user code
    return 'delete user'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8181)
