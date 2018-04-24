from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(port=5002, debug=True, ssl_context=('certificates/cert.pem', 'certificates/key.pem'))
