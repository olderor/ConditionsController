
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



c9
cd front/back
sudo pip3 install setuptools --upgrade
sudo pip3 install -r requirements.txt
+ back delete migrations folder, init db and migrate + upgrade

server.js
https://conditions-controller-olderor.c9users.io/

eg
{"tracks": [{"condition_id": 3, "value": 3, "date_recordered": "2018-05-22T09:20:00.000Z"}, {"condition_id": 4, "value": 0, "date_recordered": "2018-05-22T09:20:00.000Z"}, {"condition_id": 3, "value": 3.2, "date_recordered": "2018-05-22T09:30:00.000Z"}, {"condition_id": 4, "value": 0, "date_recordered": "2018-05-22T09:30:00.000Z"},{"condition_id": 3, "value": 3.567345, "date_recordered": "2018-05-22T09:30:00.000Z"}, {"condition_id": 4, "value": 2, "date_recordered": "2018-05-22T09:30:00.000Z"},{"condition_id": 3, "value": 5.214, "date_recordered": "2018-05-22T09:40:00.000Z"}, {"condition_id": 4, "value": 10, "date_recordered": "2018-05-22T09:40:00.000Z"},{"condition_id": 3, "value": 6, "date_recordered": "2018-05-22T09:50:00.000Z"}, {"condition_id": 4, "value": 2, "date_recordered": "2018-05-22T09:50:00.000Z"},{"condition_id": 3, "value": 6.5, "date_recordered": "2018-05-22T10:00:00.000Z"}, {"condition_id": 4, "value": 14, "date_recordered": "2018-05-22T10:00:00.000Z"},{"condition_id": 3, "value": 6.5, "date_recordered": "2018-05-22T10:10:10.000Z"}, {"condition_id": 4, "value": 12, "date_recordered": "2018-05-22T10:10:00.000Z"},{"condition_id": 3, "value": 4, "date_recordered": "2018-05-22T10:10:20.000Z"}, {"condition_id": 4, "value": 27, "date_recordered": "2018-05-22T10:10:20.000Z"}]}