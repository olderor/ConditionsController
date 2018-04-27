
export FLASK_APP=../backend/conditions_controller_context.py
flask run - run app
flask db init - create db

flask db migrate & flask db upgrade

export MAIL_SERVER=smtp.googlemail.com
export MAIL_PORT=587
export MAIL_USE_TLS=1
export MAIL_USERNAME=<your-gmail-username>
export MAIL_PASSWORD=<your-gmail-password>
export FLASK_DEBUG=1

export MAIL_SERVER=localhost
export MAIL_PORT=8025