import requests
import datetime
from tests.base_testcase import BaseTestCase


class TestForCase(BaseTestCase):
    def test_add(self):
        r = requests.post(
            'http://127.0.0.1:5000/testcase',
            json={
                'name': f'name {str(datetime.datetime.now())}',
                'description': 'd',
                'data': ''
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        print(r.text)
        print(self.token)
        assert r.status_code == 200
        assert r.json()['msg'] == 'ok'

    def test_put(self):
        r = requests.put(
            'http://127.0.0.1:5000/testcase',
            json={
                'name':"test"},
            headers={'Authorization': f'Bearer {self.token}'}

        )
        print(r.text)
        assert r.status_code == 200