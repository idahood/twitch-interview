import unittest
from app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)

    def test_twitch_asn(self):
        rv = self.app.get('/46489')
        self.assertEqual(rv.status_code, 200)

    def test_invalid_asn(self):
        rv = self.app.get('/500')
        self.assertEqual(rv.status_code, 404)

if __name__ == '__main__':
    unittest.main()
