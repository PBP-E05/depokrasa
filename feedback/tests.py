from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from feedback.models import Feedback
from feedback.forms import FeedbackForm

class FeedbackModelTest(TestCase):
    def setUp(self):
        self.feedback = Feedback.objects.create(
            subject="Test Subject",
            message="This is a test message"
        )

    def test_feedback_creation(self):
        """Test if the feedback instance is created correctly."""
        self.assertEqual(self.feedback.subject, "Test Subject")
        self.assertEqual(self.feedback.message, "This is a test message")
        self.assertIsNotNone(self.feedback.created_at)

    def test_feedback_str(self):
        """Test the string representation of the feedback model."""
        self.assertEqual(str(self.feedback), "Feedback about - Test Subject")


class FeedbackFormTest(TestCase):
    def test_feedback_form_valid_data(self):
        """Test FeedbackForm with valid data."""
        form_data = {
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_feedback_form_empty_data(self):
        """Test FeedbackForm with empty data."""
        form = FeedbackForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)
        self.assertIn('message', form.errors)


class FeedbackViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_faq_page_get_request(self):
        """Test GET request to faq_page view."""
        response = self.client.get(reverse('feedback:faq_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq.html')
        self.assertIsInstance(response.context['form'], FeedbackForm)

    def test_faq_page_post_valid_data(self):
        """Test POST request to faq_page view with valid data."""
        response = self.client.post(reverse('feedback:faq_page'), {
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True})

    def test_faq_page_post_invalid_data(self):
        """Test POST request to faq_page view with invalid data."""
        response = self.client.post(reverse('feedback:faq_page'), {
            'subject': '',  # Empty subject
            'message': ''   # Empty message
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            "success": False,
            "errors": {
                "subject": ["This field is required."],
                "message": ["This field is required."]
            }
        })
