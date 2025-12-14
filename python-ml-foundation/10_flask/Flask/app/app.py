from flask import Flask
'''
It creates an instance of the flask class,
which will be your WSGi (web server gateway interface)
'''
##WSGI application
app=Flask(__name__)

@app.route("/")
def welcome():
    return "welcome to this app anishekh"

@app.route("/index")
def index():
    return "welcome to this app anishekh 1"

@app.route("/main")
def main():
    return "welcome to this app anishekh 2"

if __name__=="__main__":
    app.run(debug=True)

