from flask import Flask,render_template,request,redirect,session,url_for
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import os
app = Flask(__name__)
app.secret_key= os.urandom(24)
app.config['MYSQL_HOST']='localhost'

app.config['MYSQL_USER']='root'

app.config['MYSQL_PASSWORD']= ''

app.config['MYSQL_DB']='chat_app'

mysql = MySQL(app)
bcrypt= Bcrypt(app)

@app.route('/')
def index():
    if 'user' in session:
        return 'u are already logged in'
    return render_template('signup.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        if 'user' in session:
            return 'u are already logged in'
        data = request.form
        username = data['username']
        password = data['password']
        pw_hash  = bcrypt.generate_password_hash(password)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username,password) values (%s,%s)", (username, pw_hash))
        mysql.connection.commit()
        cur.close()
        session['user']=username
        return redirect(url_for('protected'))
    else:
        return 'get'

@app.route('/login', methods=['POST'])
def login():
    if 'user' in session:
        return 'u are already logged in'
    forms = request.form
    username = forms['username']
    password = forms['password']
    print(username+" "+password)
    cur = mysql.connection.cursor()
    resultValue = cur.execute(" select * from users where username ='%s' " %(username))
    userDetails = cur.fetchall()
    print(resultValue)
    print(userDetails)
    check=bcrypt.check_password_hash(userDetails[0][1], password)
    if check:
        session['user']=username
    else:
        return 'password did not match!'

    return 'u are logged in!'


@app.route('/protected')
def protected():
    if 'user' in session:
        return 'success'
    else:
        return 'cupid stupid u cant code'

@app.route('/logout')
def logout():
    session.pop('user', None)
    return 'logged out!'


@app.route('/chatoptions')
def chatoptions():
    if 'user' in session:
        cur= mysql.connection.cursor()
        username = str(session['user'])
        resultValue = cur.execute(" select * from users where username <>'%s' " %(username))
        if resultValue>0:
            options=cur.fetchall()

            return render_template('chat_options.html',options=options)

if(__name__=='__main__'):
    app.run(debug=True)

