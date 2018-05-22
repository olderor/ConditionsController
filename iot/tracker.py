import requests, json
from datetime import datetime
from random import randint
import threading
from time import sleep


class Tracker:
    def __init__(self, condition_id, generator):
        self.condition_id = condition_id
        self.fs = []
        self.generator = generator
        threading.Timer(1.0, self.track).start()

    def set_tracking_event(self, f):
        self.fs.append(f)

    def track(self):
        value = self.generator.next()
        for f in self.fs:
            f(self.condition_id, value, datetime.utcnow())
        threading.Timer(1.0, self.track).start()


class Generator:
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val
        self.current = (max_val + min_val) / 2
        self.step = (max_val - min_val) / 20

    def next(self):
        if self.current > self.max_val * 1.2:
            self.current -= self.step
        elif self.current < self.min_val * 0.8:
            self.current += self.step
        elif randint(0, 1) == 0:
            self.current += self.step
        else:
            self.current -= self.step
        return self.current


class Device:
    def __init__(self, condition_datas, key, password):
        self.trackers = []
        self.key = key
        self.password = password
        self.token = None
        for condition_data in condition_datas:
            generator = Generator(condition_data['min_value'], condition_data['max_value'])
            tracker = Tracker(condition_data['id'], generator)
            self.trackers.append(tracker)
            tracker.set_tracking_event(self.track_value)

    def get_token(self):
        if self.token is None:
            self.token = ServerManager.login_device(self.key, self.password)
        return self.token

    def track_value(self, condition_id, value, date):
        ServerManager.send_track(self.get_token(), condition_id, value, date)


class ServerManager:
    # host = "https://127.0.0.1:5002"
    host = "https://conditions-controller-olderor.c9users.io"

    @staticmethod
    def send_track(token, condition_id, value, date):
        requests.post(ServerManager.host + '/api/track',
                      json={'condition_id': condition_id, 'value': value, 'date_recordered': str(date)},
                      headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token})

    @staticmethod
    def login_device(key, password):
        r = requests.post(ServerManager.host + '/api/login-device',
                          json={'key': key, 'password': password})
        json_data = json.loads(r.text)
        return json_data['token']



device = Device([{'id': 7, 'min_value': 55, 'max_value': 59}, {'id': 8, 'min_value': 55, 'max_value': 75}], 'a', 'a')
sleep(100)
