from flask import Flask, request, render_template, redirect, url_for, flash, session
import secrets
from functools import wraps

secret_key = secrets.token_hex(16)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Anda perlu masuk untuk mengakses halaman ini.')
            return redirect(url_for('hasil'))
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

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
        session['user'] = user
        flash('Berhasil login')
        return redirect(url_for('hasil'))
    return render_template('login.html')

@app.route('/buatakun', methods=['GET', 'POST'])
def buat():
    return render_template('buat.html')

@app.route('/keluar')
def keluar():
    session.pop('user', None)
    return redirect(url_for('hasil'))

if __name__ == '__main__':
    app.run(debug=True)
