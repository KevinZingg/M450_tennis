from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_court, name='book_court'),
    path('success/', views.booking_success, name='booking_success'),
    path('failed/', views.booking_failed, name='booking_failed'),
    path('', views.view_bookings, name='booking/view_bookings'),
]
