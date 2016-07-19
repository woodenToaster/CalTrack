import os
import unittest

from config import basedir
from caltrack import app, db
from caltrack.models import Ingredient

from populate_db import populate_ingredients


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

    def login(self, username, password):
        data = {
            'username': username,
            'password': password
        }
        return self.app.post('/login', data=data, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login(self):
        response = self.login('test_user', 'pw')
        self.assertTrue("You were logged in" in response.get_data(as_text=True))

    def test_populate_db(self):
        ingr = Ingredient.query.filter_by(name='broccoli').first()
        self.assertTrue(ingr is None)

        populate_ingredients()

        ingr = Ingredient.query.filter_by(name='broccoli').first()
        self.assertTrue(ingr.name == 'broccoli')
        ingr = Ingredient.query.filter_by(name='sweet potato, baked').first()
        self.assertTrue(ingr.name == 'sweet potato, baked')

if __name__ == '__main__':
    unittest.main()
