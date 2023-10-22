from flask import Flask, request, render_template, redirect, url_for, flash, session

import secrets
secret_key = secrets.token_hex(16)
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
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
@login_required

def penjumlahan():

    if request.method == 'POST':
        user = request.form['angka1']
        session['user'] = user
       
        flash('berhasil logn')
    return render_template('result.html', user =  user)


@app.route('/buatakun', methods=['GET', 'POST'])
def buat():
    return render_template('buat.html')


@app.route('/keluar')
def keluar():
    # Hapus informasi sesi
    session.pop('user', None)
    return redirect(url_for('hasil'))

if __name__ == '__main__':
    print("apk berjalan")
    app.run(debug=True)
    
