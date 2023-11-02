# views.py
from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import Booking

def book_court(request):
    if not request.user.is_authenticated:
        return redirect('booking_failed')

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('booking_success')
        else:
            # This is the case when form is not valid.
            return redirect('booking_failed')
    else:
        form = BookingForm()
    return render(request, 'book_court.html', {'form': form})


def booking_success(request):
    return render(request, 'success.html')

def booking_failed(request):
    return render(request, 'failed.html')


def view_bookings(request):
    bookings = Booking.objects.all().order_by('start_time')
    return render(request, 'view_bookings.html', {'bookings': bookings})
