import os
import tempfile
from unittest import TestCase
from django.conf import settings
from django.core.files import File
from urllib.parse import urljoin
from articles.storage import CustomStorage  # Replace with your actual import

class CustomStorageTest(TestCase):
    
    def setUp(self):
        # Set up a temporary file for testing
        self.test_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_file.write(b'This is a test file.')  # Write some test data
        self.test_file.close()  # Close the file so it can be used by FileStorage

        # Create an instance of CustomStorage
        self.storage = CustomStorage()

    def tearDown(self):
        # Clean up the test file
        if os.path.exists(self.test_file.name):
            os.remove(self.test_file.name)

    def test_save_file(self):
        # Test saving the file
        with open(self.test_file.name, 'rb') as f:
            file = File(f, name='test_file.txt')
            saved_name = self.storage.save(file.name, file)
        
        # Check if the file has been saved
        saved_path = os.path.join(self.storage.location, saved_name)
        self.assertTrue(os.path.exists(saved_path))

        # Clean up saved file
        os.remove(saved_path)

    def test_exists(self):
        # Save the file first
        with open(self.test_file.name, 'rb') as f:
            file = File(f, name='test_file.txt')
            saved_name = self.storage.save(file.name, file)

        # Test if the file exists
        self.assertTrue(self.storage.exists(saved_name))

        # Clean up saved file
        os.remove(os.path.join(self.storage.location, saved_name))

    def test_location_and_base_url(self):
        # Test the location and base URL
        self.assertEqual(self.storage.location, os.path.join(settings.MEDIA_ROOT, "articles"))
        self.assertEqual(self.storage.base_url, urljoin(settings.MEDIA_URL, "articles/"))