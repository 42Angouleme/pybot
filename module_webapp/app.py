import sqlite3
from flask import Flask, Blueprint, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET KEY'] = 'secret'

auth = Blueprint('auth', __name__)

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return  connection

@auth.route('/login')
def login():
    return 'Login'

@auth.route('/signup')
def signup():
    return 'Signup'

@auth.route('/logout')
def logout():
    return 'Logout'
@app.route('/')
def login_page():
    return render_template("login.html", name="")

@app.route('/index')
def index_page():
    return render_template("index.html", name="")

@app.route('/name')
def profile_page():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM name').fetchall()
    connection.commit()
    connection.close()
    return render_template("name.html", posts=posts, image="test.jpg")

@app.route('/search')
def search_page():
    return render_template("search.html")

@app.route('/add', methods=('GET', 'POST'))
def add_page():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM name').fetchall()
    connection.commit()
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['firstname']
        if name and surname:
            posts = connection.execute('SELECT * FROM name').fetchall()
            connection.execute('INSERT INTO name(name, firstname) VALUES (?, ?)', (name, surname))
            connection.commit()
            connection.close()
            return redirect(url_for('profile_page'))

    return render_template("add.html", posts=posts)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8181)
