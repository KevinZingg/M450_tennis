from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Member
from .forms import RegisterForm
from django.contrib.auth import authenticate, login as auth_login


def members(request):
    members = Member.objects.all()
    print(members)  # Debugging
    return render(request, 'all_members.html', {'members': members})


def details(request, id):
    member = Member.objects.get(id=id)
    return render(request, 'details.html', {'member': member})



def main(request):
    return render(request, 'main.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Log the user in or redirect to a success page
            return redirect('main')  # Change this as per your needs
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            print("user logged in")
            return redirect('main')
        else:
            # Invalid login credentials
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

