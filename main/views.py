# django-builtin modules
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import login_required
from django.shortcuts import Http404, redirect, render, reverse, HttpResponse

# custom models
from .models import (Class, ClassLesson, Student, Teacher)


def teacher_only(func):
    def wrapper(request):
        user = request.user
        if Teacher.objects.filter(user=user):
            return func(request)
        return Http404()
    return wrapper


def index(request):
    return render(request, 'main/index.htm', {})


def login_view(request):
    if request.method == 'GET':
        return render(request, 'main/login.htm')
    else:
        user = authenticate(request, password=request.POST['password'], username=request.POST['username'])
        if user:
            login(request, user)
            return redirect("/")
