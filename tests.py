import unittest
from server import app
from flask import json
from model import db, Bart, Business, Job, Save, User, connect_to_db, example_data
from api_functions import get_job_results


class WorkNearBartTests(unittest.TestCase):
    """Tests for the Work Near Bart pages"""

    def setUp(self):
        """Stuff to do before every test."""
        
        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
    
    def test_login_page(self):
        """Tests the login page"""

        result = self.client.get('/login')
        self.assertIn('Login', result.data)

    def test_register_page(self):
        """Tests the register page"""

        result = self.client.get('/register')
        self.assertIn('Register', result.data)


class WorkNearBartDBTests(unittest.TestCase):
    """Tests for the Work Near Bart pages"""

    def setUp(self):
        """Stuff to do before every test."""
        
        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_homepage(self):
        """Tests the homepage"""

        result = self.client.get('/')
        self.assertIn('<title>Work Near BART - Home</title>', result.data)

    def test_login_register_button(self):
        """If user is not logged in, do they see a login and register button?"""

        result = self.client.get('/')
        self.assertIn('<form action="/login"><button type="submit">Login</button></form>', result.data)
        self.assertIn('<form action="/register"><button type="submit">Register</button></form>', result.data)

    def test_results_page(self):
        """Tests to see if results display on page"""

        result = self.client.get('/results/1?title=software+engineer&station=EMBR&days=999&display=10')
        self.assertIn('ABC, Inc.', result.data) 

    def test_get_station(self):
        """Test if we can get a bart station"""

        emb = Bart.query.filter(Bart.station_code=="EMBR").first()
        self.assertEqual(emb.name, "Embarcadero")




class WorkNearBartSessionTests(unittest.TestCase):
    """Tests for the Work Near Bart pages"""

    def setUp(self):
        """Stuff to do before every test."""
        
        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        # Add a user to session
        # self.client.session_transaction()['user_id'] = 1

    def login(self, email, password):
        """Class method to handle logins"""
        
        return self.client.post('/login', data=dict(
            email=email,
            password=password
            ), follow_redirects=True)

    def logout(self):
        """Class method to handle logouts"""

        return self.client.post('/logout', follow_redirects=True)

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()
    
    def test_login_logout(self):
        result = self.login('test@test.com', 'test')
        self.assertIn('You are logged in as', result.data)

        result = self.logout()
        self.assertIn('Logged out.', result.data)

        result = self.login('demo@demo.com', '123')
        self.assertIn('That email does not exist.  Please register if you are a new user.', result.data)
        
        result = self.login('test@test.com', '123')
        self.assertIn('Incorrect email or password.', result.data)

    def saved_jobs_page(self):
        """Tests the saved jobs page"""

        result = self.client.get('/savedjobs')
        self.assertIn





if __name__ == "__main__":

    unittest.main()

