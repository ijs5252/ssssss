from flask import Flask, render_template, session, url_for, redirect, request

app = Flask(__name__)
app.secret_key = 'this is super key'
app.config['SESSION_TYPE'] = 'filesystem'
userinfo = {'fu': 'fu'}
board = []


@app.route("/")
def homepage():
    if session.get('logged_in') :
        return render_template('loggedin.html', rows = board)
    else:
        return render_template('index.html', rows = board)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        try:
            if name in userinfo:
                if userinfo[name] == password:
                    session['logged_in'] = True
                    return redirect(url_for('homepage'))
                else:
                    return '비밀번호 오류!'
            return '존재하지 않는 아이디입니다'
        except:
            return '다시 시도해주세요'
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def regist():
    if request.method == 'POST':
        userinfo[request.form['username']] = request.form['password']
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('index.html', rows = board)

@app.route('/board')
def loggedin_board():
    return render_template('board.html', rows = board)


@app.route('/add', methods = ['POST'])
def Board():
    if request.method == 'POST':
        board.append([request.form['title'], request.form['context'], request.form['keyword']])
        return redirect(url_for('loggedin_board'))
    else:
        return render_template('board.html', rows = board)


if __name__ == '__main__':
    app.run(debug=True)