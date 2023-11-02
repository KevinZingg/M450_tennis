from django.test import TestCase, Client
from django.urls import reverse
from .models import Member
from .forms import RegisterForm
import datetime

class MemberModelTest(TestCase):

    # Test for Member model
    def test_member_creation(self):
        # Erstellt en Member und überprüeft ob er korrekt gespeichert wird
        member = Member.objects.create(username="testuser", password="testpassword")
        self.assertIsInstance(member, Member)
        self.assertEqual(member.username, "testuser")
        self.assertEqual(member.joined_date, datetime.date.today())

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
            email="test@example.com",
            first_name="Test",
            last_name="User"
        )

    # Test für die Member-Übersicht
    def test_members_view(self):
        response = self.client.get(reverse('members'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)

    # Test für die Detailansicht eines Members
    def test_details_view(self):
        response = self.client.get(reverse('details', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    # Test für die Hauptseite
    def test_main_view(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    # Test für die Anmeldung
    def test_user_login_view(self):
        self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        # Check if the user is authenticated after login
        user_id = self.client.session.get('_auth_user_id')
        self.assertIsNotNone(user_id)
        self.assertTrue(Member.objects.filter(id=user_id).exists())

    # Test für ungültige Anmeldung
    def test_invalid_user_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

