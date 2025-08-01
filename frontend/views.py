from django.shortcuts import render


def home(request):
    return render(request, 'frontend/home.html')


def login_view(request):
    return render(request, 'frontend/login.html')
