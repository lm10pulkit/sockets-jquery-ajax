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
        return redirect(url_for('chatoptions'))
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

    return redirect(url_for('chatoptions'))


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
        else:
            'there is no one to chat'
    return redirect(url_for('index'))

@app.route('/chat/<r_username>', methods=['GET','POST'])
def chat(r_username=None):
    if 'user' not in session:
        return redirect(url_for('index'))
    reciever = str(r_username)
    sender = str(session['user'])
    cur = mysql.connection.cursor()
    if request.method=='GET':
        resultValue = cur.execute(" select * from users where username ='%s' " % (r_username))
        if 'user' in session:
            if resultValue ==0:
                return '<h2>No user of this username registered</h2>'
            elif r_username==session['user']:
                return '<h2>Come on dawg! u cant send urself a message</h2>'
            else:
                dict={}
                dict['reciever']=str(r_username)

                select_stmt = ("select * from messages where (sender = (%s) and reciever=(%s)) or (sender = (%s) and reciever=(%s))")
                data =(sender,reciever,reciever,sender)
                cur.execute(select_stmt,data)
                dict['messages']=cur.fetchall()
                print(dict['messages'])
                return render_template('chat.html',Details=dict)
        else:
            return redirect(url_for('index'))
    else:
        if 'user' in session:
            message = str(request.form['message'])
            cur.execute("INSERT INTO messages (sender,reciever,message) values (%s,%s,%s)" ,(sender,reciever,message))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('chat',r_username=reciever))
        else:
            return redirect(url_for('index'))




if(__name__=='__main__'):
    app.run(debug=True)

