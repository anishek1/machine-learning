from flask import Flask,render_template
'''
It creates an instance of the flask class,
which will be your WSGi (web server gateway interface)
'''
##WSGI application
app=Flask(__name__)

@app.route("/")
def welcome():
    return "<html><H1>welcome to my page<H!></html>"

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/main")
def main():
    return render_template('about.html')

if __name__=="__main__":
    app.run(debug=True)

