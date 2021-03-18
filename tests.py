from unittest import TestCase

from app import app
from flask_bcrypt import Bcrypt
from models import db, connect_db, User, Board, Piece

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dndboard'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

USER_DATA_1 = {
    "username":"Test",
    "email":"test@gmail.com",
    "password":bcrypt.generate_password_hash("testword").decode('UTF-8'),
    "first_name":"Test"
    "last_name": "Tester"
}

USER_DATA_2 = {
    "username":"TestAid",
    "email":"testaid@gmail.com",
    "password":bcrypt.generate_password_hash("testword").decode('UTF-8'),
    "first_name":"Test"
    "last_name": "Ruiner"
}

USER_DATA_3 = {
    "username":"TestAid",
    "email":"testaid@gmail.com",
    "password":bcrypt.generate_password_hash("testword").decode('UTF-8'),
    "first_name":"Test"
    "last_name": "Ruiner"
}

class DNDSourcesTestCases(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        User.query.delete()

        user = User(USER_DATA_1)
        db.session.add(user)
        db.session.commit()

        self.user = user

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()
    #WE don't need to test the external APIs, but we need to confirm our endpoints poitng to them works
    def test_list_monsters(self):
        with app.test_client() as client:
            resp = client.get("/monsters")
            self.assertEqual(resp.status_code, 200)
    
    def test_get_monster(self):
        with app.test_client() as client:
            resp = client.get("/monsters/aboleth")
            self.assertEqual(resp.status_code, 200)

    def test_list_spells(self):
        with app.test_client() as client:
            resp = client.get("/spells")
            self.assertEqual(resp.status_code, 200)

    def test_get_spell(self):
        with app.test_client() as client:
            resp = client.get("/spells/acid-arrow")
            self.assertEqual(resp.status_code, 200)

    def test_create_user(self):
        with app.test_client() as client:
            url = "/signup"
            resp = client.post(url, form=USER_DATA_3)
            self.assertEqual(resp.status_code, 201)
            data = resp.json

            self.assertIsInstance(data['user']['id'], int)
            del data['user']['id']

            self.assertEqual(data, {
                USER_DATA_3
            })

            self.assertEqual(User.query.count(), 2)

   def test_edit_user(self):
        with app.test_client() as client:
            url = "/profile/edit"
            resp = client.post(url, form=USER_DATA_2)
            self.assertEqual(resp.status_code, 201)
            data = resp.json

            self.assertIsInstance(data['user']['id'], int)
            del data['user']['id']

            self.assertEqual(data, {
                USER_DATA_2
            })

            self.assertEqual(User.query.count(), 2)

   def test_login(self):
        with app.test_client() as client:
            url = "/login"
            resp = client.post(url, form=USER_DATA_1)
            self.assertEqual(resp.status_code, 200)
            data = resp.json

            self.assertIsInstance(data['user']['id'], int)
            del data['user']['id']

            self.assertEqual(data, {
                USER_DATA_2
            })

            self.assertEqual(User.query.count(), 2)