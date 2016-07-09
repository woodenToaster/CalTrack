import os
import caltrack
import unittest
import tempfile


class CalTrackTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, caltrack.app.config['DATABASE'] = tempfile.mkstemp()
        caltrack.app.config['TESTING'] = True
        self.app = caltrack.app.test_client()
        with caltrack.app.app_context():
            caltrack.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(caltrack.app.config['DATABASE'])

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
        rv = self.login('admin', 'default')
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert b'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert b'Invalid password' in rv.data

    def test_messages(self):
        self.login('admin', 'default')
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
        assert b'broccoli' in rv.data
        assert b'50' in rv.data

if __name__ == '__main__':
    unittest.main()
