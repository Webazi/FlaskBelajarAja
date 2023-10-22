from flask import Flask, request, render_template, redirect, url_for, flash, session, redirect

import secrets

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key


@app.route('/', methods=['GET', 'POST'])
def hasil():
    
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def penjumlahan():
    hasil = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['pw']
        flash(f'berhasil login ke  {name} ')
        session['user'] = name
    if 'user' in session:
        return redirect(url_for('/'))
    if 'user' not in session:
        return redirect(url_for('login'))
   
       
    return render_template('result.html', hasil=hasil)


@app.route('/buatakun', methods=['GET', 'POST'])
def buat():
    return render_template('buat.html')
if __name__ == '__main__':
    print("apk berjalan")
    app.run(debug=True)
    
