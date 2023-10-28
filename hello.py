from flask import Flask, request, render_template, redirect, url_for, flash, session
import secrets
from functools import wraps
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash

secret_key = secrets.token_hex(16)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Anda perlu masuk untuk mengakses halaman ini.', 'danger')
            return redirect(url_for('hasil'))
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] ='akun'
mysql = MySQL(app)



@app.route('/', methods=['GET', 'POST'])
def hasil():
    if 'user' in session:
        user = session['user']
        return render_template('result.html', user=user)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        email = request.form['email']
        pw = request.form['pw']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username=%s OR email=%s ',(user,email))
        akun = cursor.fetchone()
        print(akun)
        if akun is None:
            cursor.execute('INSERT INTO user VALUES (NULL, %s,%s,%s)',(user,email,generate_password_hash(pw)))
            cursor.connection.commit()
            
        else:
            flash('udah ada akunnya','danger')
        session['user'] = user
        flash(f'selamat datang {user}')
    
        return redirect(url_for('hasil'))
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['pw']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username=%s OR email=%s ',(user,email))
        akun = cursor.fetchone()
        return redirect(url_for('hasil'))
    return render_template('index.html')
@app.route('/buatakun', methods=['GET', 'POST'])
def buat():
    return render_template('buat.html')

@app.route('/keluar')
def keluar():
    session.pop('user', None)
    return redirect(url_for('hasil'))

@app.route('/upload')
def upload():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
