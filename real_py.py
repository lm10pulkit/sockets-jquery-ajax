from flask import Flask , render_template, request


app= Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    if request.method=="POST":
        print(request.form)
    return render_template('main.html')
if __name__=='__main__':
    app.run(debug =True)

