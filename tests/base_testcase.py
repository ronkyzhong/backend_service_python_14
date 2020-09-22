import requests


class BaseTestCase:
    def setup_class(self):
        username = 'ronky'
        password = 'ronky123'
        r = requests.post(
            'http://127.0.0.1:5000/login',
            json={
                'username': username,
                'password': password
            }
        )
        self.token = r.json()['token']