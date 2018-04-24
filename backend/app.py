from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
import bcrypt

mysql = MySQL()
app = Flask(__name__)


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password, hashed_password)


class Response:
    def __init__(self, data=None, errors=list()):
        self.errors = errors
        self.data = data

    def success(self):
        return len(self.errors) == 0

    def __str__(self):
        json.dumps({'success': self.success(), 'errors': self.errors, 'data': self.data})


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/sign-up', methods=['POST'])
def sign_up():
    try:
        email = request.form['email']
        password = request.form['password']

        # validate the received values
        if not (email and password):
            return Response(errors=['Specify email or password to register.'])

        conn = mysql.connect()
        cursor = conn.cursor()
        hashed_password = get_hashed_password(password)
        cursor.callproc('sp_createUser', (email, hashed_password))
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return Response(data={'message': 'User was created.'})
        else:
            return Response(errors=data[0])

    except Exception as e:
            return Response(errors=[str(e)])
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # Cloud9 setup.
    app.run(host='0.0.0.0', port=8080, debug=True)
    # app.run(port=5002, debug=True, ssl_context=('certificates/cert.pem', 'certificates/key.pem'))
