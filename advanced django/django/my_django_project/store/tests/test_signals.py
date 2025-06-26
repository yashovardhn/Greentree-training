from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
import logging

User = get_user_model()

class UserSignalsTest(TestCase):
    def setUp(self):
        # Set up a test logger
        self.logger = logging.getLogger('store.signals')
        self.handler = logging.StreamHandler()
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.INFO)
        self.handler.setLevel(logging.INFO)
        
        # Capture log output
        from io import StringIO
        self.log_output = StringIO()
        self.handler.stream = self.log_output

    def test_user_creation_logs_message(self):
        """Test that creating a user logs the expected message"""
        # Create a test user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Check the log output
        log_content = self.log_output.getvalue()
        self.assertIn(f"New user created: {user.username} (ID: {user.id})", log_content)
        
    def tearDown(self):
        # Clean up the logger
        self.logger.removeHandler(self.handler)
        self.handler.close()
