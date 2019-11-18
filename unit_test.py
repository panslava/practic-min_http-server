import requests
import unittest

BASE_URL = 'http://localhost:65432'


class TestCase(unittest.TestCase):

    def test_1_Create(self):
        data = {
            'key': 1,
            'value': 'Hello'
        }
        response = requests.post(f'{BASE_URL}/put', data=data)
        self.assertEqual(response.status_code, 200)

    def test_2_GetExistNotCached(self):
        response = requests.get(f'{BASE_URL}/get?key=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['value'], 'Hello')

    def test_3_Update(self):
        data = {
            'key': 1,
            'value': 'World'
        }
        response = requests.put(f'{BASE_URL}/put', data=data)
        self.assertEqual(response.status_code, 200)

    def test_4_GetOldCached(self):
        response = requests.get(f'{BASE_URL}/get?key=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['value'], 'Hello')

    def test_5_GetNewNoCache(self):
        response = requests.get(f'{BASE_URL}/get?key=1&no-cache=true')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['value'], 'World')

    def test_6_GetNotExist(self):
        response = requests.get(f'{BASE_URL}/get?key=2')
        self.assertEqual(response.status_code, 404)

    def test_7_Delete(self):
        response = requests.delete(f'{BASE_URL}/delete?key=1')
        self.assertEqual(response.status_code, 200)

    def test_8_CheckDeleted(self):
        response = requests.get(f'{BASE_URL}/get?key=1')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
