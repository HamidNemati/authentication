from flask import Flask, render_template, request
import sqlite3
import jwt

app = Flask(__name__)
conn = sqlite3.connect('database.db')
print('database opened successfully!')

conn.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, email TEXT, age TEXT)')
print('"users" table has created successfully!')
conn.close()

key = 'coding_key'
tokens =[]


@app.route('/')
def hello_world():
    return render_template('init.html')


@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('signin.html', username_check=None)
    
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    age = request.form.get('age')
    if username:
        print('{}, {}, {}, {}'.format(username, password, email, age))
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            result = cur.execute('SELECT * FROM users WHERE username=?',(username,))
            if len(result.fetchall()) > 0:
                return render_template('signin.html', username_check=False)
            
            cur.execute('INSERT INTO users (username, password, email, age) VALUES (?,?,?,?)',(username, password, email, age))
            print('{} added to database!'.format(username))
            return username+' added!'
    return 'NONE INPUT!'

@app.route('/log_in')
def log_in(wrong=None):
    return render_template('login.html', last_tried=wrong)
    


@app.route('/login_check')
def check_validity():
    username = request.args.get('username')
    password = request.args.get('password')
    print('{} , password: {} is trying to login!'.format(username, password))
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        result = cur.execute('SELECT * FROM users WHERE username=? and password=?',(username,password,))
        if len(result.fetchall()) > 0:
            token = jwt.encode({'username':username, 'password':password}, key, algorithm="HS256")
            if tokens.count(token) > 0:
                return 'You Are Already Inside Your Account!'
            
            tokens.append(token)
            return 'WELCOME {}. your token is {}'.format(username, token)


    return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True)
