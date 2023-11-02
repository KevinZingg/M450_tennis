from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'class': 'datetimepicker'}),
        input_formats=['%Y-%m-%d %H:%M:%S']
    )
    end_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'class': 'datetimepicker'}),
        input_formats=['%Y-%m-%d %H:%M:%S']
    )

    class Meta:
        model = Booking
        fields = ['court', 'start_time', 'end_time']
