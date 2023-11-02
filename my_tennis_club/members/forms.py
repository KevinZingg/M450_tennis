from django.contrib.auth.forms import UserCreationForm
from .models import Member

class RegisterForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ['username', 'first_name', 'last_name', 'phone', 'email', 'password1', 'password2']
