import os
import unittest

from config import basedir
from caltrack import app, db


class CalTrackTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No ingredients yet' in rv.data

    def login(self, username, password):
        data = {
            'username': username,
            'password': password
        }
        return self.app.post('/login', data=data, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('chris', 'hi')
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert b'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        # assert b'Invalid password' in rv.data

    def test_messages(self):
        self.login('chris', 'hi')
        data = {
            'name': 'broccoli',
            'calories': '50',
            'protein': '4',
            'carbs': '10',
            'fat': '1',
            'fiber': '4'
        }
        rv = self.app.post('/add', data=data, follow_redirects=True)
        assert b'No ingredients yet' not in rv.data
        # assert b'broccoli' in rv.data
        # assert b'50' in rv.data

if __name__ == '__main__':
    unittest.main()
