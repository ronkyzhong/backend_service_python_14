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
            'http://127.0.0.1:5000/testcase/1',
            json={
                "id": 1,
                'name': "zjs"
            },
            headers={'Authorization': f'Bearer {self.token}'}

        )
        print(r.text)
        assert r.status_code == 200

    def test_delete(self):
        r = requests.delete(
            'http://127.0.0.1:5000/testcase/4',
            headers={'Authorization': f'Bearer {self.token}'}

        )
        assert r.status_code == 200

    def test_delete_except(self):
        r = requests.delete(
            'http://127.0.0.1:5000/testcase/100',
            headers={'Authorization': f'Bearer {self.token}'}

        )
        assert r.json()['errmsg'] == '用例不存在不能进行删除'
        assert r.json()['errcode'] == 0
