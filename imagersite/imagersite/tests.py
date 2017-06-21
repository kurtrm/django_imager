"""Tests for config route and registration."""
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django.core import mail
from bs4 import BeautifulSoup
from imagersite.views import home_view
import factory


class Registration(TestCase):
    """Tests for registration process."""

    def client_setup(self):
        """Create a client instance."""
        self.client = Client()

    def test_registration_template(self):
        """Test registration route uses registration template."""
        response = self.client.get(reverse('registration_register'))
        self.assertIn('registration/registration_form.html', response.template_name)

    def test_check_new_user_created_after_registration(self):
        """Test that a new user is created after registration."""
        self.assertTrue(User.objects.count() == 0)
        response = self.client.get(reverse('registration_register'))
        html = BeautifulSoup(response.rendered_content, 'html.parser')

        token = html.find('input', {'name': 'csrfmiddlewaretoken'}).attrs['value']

        data_dict = {
            'csrfmiddlewaretoken': token,
            'username': 'morgan',
            'email': 'morgan@morgan-nomura.com',
            'password1': 'helloiammorgan',
            'password2': 'helloiammorgan'
        }
        self.client.post(
            reverse('registration_register'),
            data_dict
        )
        self.assertTrue(User.objects.count() == 1)

    def test_new_user_is_inactive_on_creation(self):
        """Test that new user is inactive by default."""
        response = self.client.get(reverse('registration_register'))
        html = BeautifulSoup(response.rendered_content, 'html.parser')

        token = html.find('input', {'name': 'csrfmiddlewaretoken'}).attrs['value']

        data_dict = {
            'csrfmiddlewaretoken': token,
            'username': 'morgan',
            'email': 'morgan@morgan-nomura.com',
            'password1': 'helloiammorgan',
            'password2': 'helloiammorgan'
        }
        self.client.post(
            reverse('registration_register'),
            data_dict
        )
        self.assertFalse(User.objects.first().is_active)

    def test_registration_email_sent(self):
        """Test that an email exists after a user registers successfully."""
        response = self.client.get(reverse('registration_register'))
        html = BeautifulSoup(response.rendered_content, 'html.parser')

        token = html.find('input', {'name': 'csrfmiddlewaretoken'}).attrs['value']

        self.assertEquals(len(mail.outbox), 0)

        data_dict = {
            'csrfmiddlewaretoken': token,
            'username': 'morgan',
            'email': 'morgan@morgan-nomura.com',
            'password1': 'helloiammorgan',
            'password2': 'helloiammorgan'
        }
        self.client.post(
            reverse('registration_register'),
            data_dict
        )
        self.assertEquals(len(mail.outbox), 1)


class LoginLogout(TestCase):
    """Tests for login / logout process."""

    def setUp(self):
        """Create a client instance."""
        self.client = Client()
        self.req_factory = RequestFactory()

    def test_home_view_returns_status_code_200(self):
        """Test home view has status 200."""
        # import pdb; pdb.set_trace()
        get_req = self.req_factory.get('/')
        response = home_view(get_req)
        self.assertTrue(response.status_code == 200)
