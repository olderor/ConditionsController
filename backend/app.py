from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    # Cloud9 setup.
    # app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(port=5002, debug=True, ssl_context=('certificates/cert.pem', 'certificates/key.pem'))
