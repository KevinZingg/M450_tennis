from django.test import TestCase
from django.contrib.auth.models import User
from .models import TennisCourt, Booking
from .forms import BookingForm
from django.urls import reverse, resolve
from .views import book_court, booking_success, booking_failed, view_bookings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class TennisCourtModelTest(TestCase):
    def test_string_representation(self):
        court = TennisCourt(name='Court 1')
        self.assertEqual(str(court), court.name)

class BookingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='12345')
        cls.court = TennisCourt.objects.create(name='Court 1')
        cls.booking = Booking.objects.create(
            user=cls.user,
            court=cls.court,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1)
        )

    def test_string_representation(self):
        self.assertEqual(
            str(self.booking),
            f'{self.booking.court.name} booked by {self.booking.user.username} on {self.booking.start_time}'
        )

class BookingFormTest(TestCase):
    def test_form_date_field_label(self):
        form = BookingForm()
        self.assertTrue(form.fields['start_time'].label is None or form.fields['start_time'].label == 'start time')
        self.assertTrue(form.fields['end_time'].label is None or form.fields['end_time'].label == 'end time')

    def test_form_validation_for_blank_items(self):
        form = BookingForm(data={'start_time': '', 'end_time': ''})
        self.assertFalse(form.is_valid())

class BookingViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='12345')
        cls.court = TennisCourt.objects.create(name='Court 1')

    def test_book_court_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('book_court'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_court.html')

    def test_booking_success_view(self):
        response = self.client.get(reverse('booking_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')

    def test_view_bookings_view(self):
        response = self.client.get(reverse('booking/view_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_bookings.html')

class URLTest(TestCase):
    def test_book_court_url(self):
        path = reverse('book_court')
        assert resolve(path).view_name == 'book_court'

    def test_booking_success_url(self):
        path = reverse('booking_success')
        assert resolve(path).view_name == 'booking_success'

    def test_booking_failed_url(self):
        path = reverse('booking_failed')
        assert resolve(path).view_name == 'booking_failed'

    def test_view_bookings_url(self):
        path = reverse('booking/view_bookings')
        assert resolve(path).view_name == 'booking/view_bookings'
