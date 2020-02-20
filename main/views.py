from django.shortcuts import render, Http404, reverse, redirect
from django.contrib.auth.views import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Student, Teacher


def teacher_only(func):
    def wrapper(request):
        user = request.user
        if Teacher.objects.filter(user=user):
            return func(request)
        return Http404()
    return wrapper


def index(request):
    return render(request, 'main/index.htm', {})


@login_required
@teacher_only
def attendance(request):
    return render(request, 'main/attendance.htm', {'class': request.user.teacher.has_class()})


def login_view(request):
    if request.method == 'GET':
        return render(request, 'main/login.htm')
    else:
        user = authenticate(request, password=request.POST['password'], username=request.POST['username'])
        if user:
            login(request, user)
            return redirect("/")
