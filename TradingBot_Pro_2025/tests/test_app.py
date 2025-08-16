import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import app

class AppTestCase(unittest.TestCase):
    """
    Test case for the Flask application.
    """

    def setUp(self):
        """Set up a test client for the Flask application."""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_bot_status(self):
        """Test the /api/status endpoint."""
        response = self.app.get('/api/status')
        self.assertEqual(response.status_code, 200)
        self.assertIn('bot_status', response.json)

    def test_toggle_bot(self):
        """Test the /api/toggle-bot endpoint."""
        # Test turning ON
        response = self.app.post('/api/toggle-bot')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'ON')

        # Test turning OFF
        response = self.app.post('/api/toggle-bot')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'OFF')

    def test_get_compliance_status(self):
        """Test the /api/compliance/status endpoint."""
        response = self.app.get('/api/compliance/status')
        self.assertEqual(response.status_code, 200)
        self.assertIn('checked_regulations', response.json)
        self.assertEqual(response.json['status'], 'OK')

if __name__ == '__main__':
    unittest.main()
