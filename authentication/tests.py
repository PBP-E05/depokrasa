from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import UserProfile
from .forms import UserRegistrationForm

class AuthenticationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('authentication:register')
        self.login_url = reverse('authentication:login')
        self.logout_url = reverse('authentication:logout')
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, email='testuser@example.com')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post_valid(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_post_invalid(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'wrongpassword',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:show_main'))
        self.assertTrue(self.client.cookies['last_login'])

    def test_login_view_post_invalid(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Invalid username or password.')

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.email, 'testuser@example.com')

    def test_user_profile_str(self):
        self.assertEqual(str(self.user_profile), 'testuser')

    def test_user_profile_default_picture(self):
        self.assertEqual(self.user_profile.profile_picture.name, 'profile_pictures/default.jpg')

    def test_register_existing_username(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'A user with that username already exists.')

    def test_register_invalid_email(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'invalid-email'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'Enter a valid email address.')

    def test_login_nonexistent_username(self):
        response = self.client.post(self.login_url, {
            'username': 'nonexistentuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Invalid username or password.')

    def test_user_profile_update(self):
        self.user_profile.email = 'updated@example.com'
        self.user_profile.save()
        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.email, 'updated@example.com')

    def test_user_profile_deletion(self):
        self.user_profile.delete()
        self.assertFalse(UserProfile.objects.filter(user=self.user).exists())