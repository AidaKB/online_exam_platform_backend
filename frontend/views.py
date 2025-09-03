from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'frontend/home.html')


def login_view(request):
    return render(request, 'frontend/login.html')


@login_required
def institute_dashboard(request):
    return render(request, 'frontend/institute_dashboard.html')


@login_required
def teacher_dashboard(request):
    return render(request, 'frontend/teacher_dashboard.html')


def add_class_view(request):
    return render(request, 'frontend/add_classes.html')
