from django.test import TestCase
from .models import Member
from .forms import RegisterForm
from django.test import TestCase, Client
from django.urls import reverse
import datetime


class MemberModelTest(TestCase):

    # Test for Member model
    def test_member_creation(self):
        # Erstellt en Member und überprüeft ob er korrekt gespeichert wird
        member = Member.objects.create(username="testuser", password="testpassword")
        self.assertIsInstance(member, Member)
        self.assertEqual(member.username, "testuser")
        self.assertEqual(member.joined_date, datetime.date.today())

        # Test


class RegisterFormTest(TestCase):

    # Test für RegisterForm mit gültigen Daten
    def test_valid_form(self):
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = RegisterForm(data)
        self.assertTrue(form.is_valid())

    # Test für RegisterForm mit ungültigen Daten
    def test_invalid_form(self):
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890',
            'email': 'test@example.com',
            # Die Passwörter stimmen nicht überein
            'password1': 'testpassword1',
            'password2': 'testpassword2',
        }
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())

class ViewTest(TestCase):
    def setUp(self):
        # Setzt en Test Client uf und erstellt en Test User
        self.client = Client()
        self.user = Member.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com"
        )

    # Test für die Member-Übersicht
    def test_members_view(self):
        response = self.client.get(reverse('members'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")

    # Test für die Detailansicht eines Members
    def test_details_view(self):
        response = self.client.get(reverse('details', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")

    # Test für die Hauptseite
    def test_main_view(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    # Test für die Registrierung
    def test_register_view(self):
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'phone': '9876543210',
            'email': 'new@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  # Sollte zur Hauptseite weiterleiten
        self.assertTrue(Member.objects.filter(username='newuser').exists())

    # Test für die Anmeldung
    def test_user_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Sollte zur Hauptseite weiterleiten
        self.assertTrue(response.context['user'].is_authenticated)

    # Test für ungültige Anmeldung
    def test_invalid_user_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)