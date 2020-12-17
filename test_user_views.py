"""User views tests."""

# run these tests like:
#
#  FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app, InvalidRequestError, IntegrityError

app.config["WTF_CSRF_ENABLED"] = False

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Test views for the user."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="PASSWORD",
            image_url="http://google.com",
        )

        db.session.commit()

        u2 = User.signup(
            email="test2@test.com",
            username="testuser2",
            password="PASSWORD2",
            image_url="http://google.com",
        )

        db.session.commit()

        self.u1 = u
        self.u2 = u2
        self.u1_username = u.username

        self.client = app.test_client()

        self.login_data = {
            "username": self.u1_username,
            "password": "PASSWORD"
        }
    
    def tearDown(self):
        """ Clean up test database """

        db.session.rollback()

    def test_login(self):
        """ Test that the login form correctly displays and
            user with valid credentials can log in """

        resp = self.client.get("/login")
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('id="login_form"', html)

        login_data = {
            "username": self.u1_username,
            "password": "PASSWORD"
        }

        resp = self.client.post("/login", data=login_data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(f'Hello, {self.u1_username}!', html)
        self.assertIn(f'@{self.u1_username}', html)
    





    

# When you’re logged in, can you see the follower / following pages for any user? YES
# When you’re logged out, are you disallowed from visiting a user’s follower / following pages? YES
# When you’re logged in, can you add a message as yourself? YES
# When you’re logged in, can you delete a message as yourself? AS LONG AS ITS YOURS
# When you’re logged out, are you prohibited from adding messages? YES
# When you’re logged out, are you prohibited from deleting messages? YES
# When you’re logged in, are you prohibiting from adding a message as another user? YES
# When you’re logged in, are you prohibiting from deleting a message as another user? YES