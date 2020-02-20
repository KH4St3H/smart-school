from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import login_required
from django.shortcuts import Http404, redirect, render, reverse, HttpResponse

from .models import (Class, ClassLesson, Student,
                     StudentPrecense, Teacher)

import datetime


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
    if request.method=='GET':
        current_class = request.user.teacher.has_class()
        if current_class:
            prev_attendence = StudentPrecense.objects.filter(class_lesson=current_class, date=datetime.date.today())
            if prev_attendence:
                states = prev_attendence
            else:
                prev_class = current_class.has_previous_class()
                if prev_class:
                    attendance_list = StudentPrecense.objects.filter(class_lesson=prev_class[0], date=datetime.date.today())
                    if attendance_list:
                        states = attendance_list
                    else:
                        states = False
                else:
                    states = False
            return render(request, 'main/attendance.htm', {'class': current_class.related_class, 'states': states})
        else:
            return render(request, 'main/attendance.htm', {'class': False, 'states': False})

    elif request.method=='POST':
        current_class = request.user.teacher.has_class()
        prev_attendence = StudentPrecense.objects.filter(class_lesson=current_class, date=datetime.date.today())
        i = 0
        for student in current_class.related_class.student_set.all():
            presence = True if request.POST.getlist('states[]')[i]=='true' else False
            i+=1
            if prev_attendence:
                obj = prev_attendence.filter(student=student)[0]
                if obj.present==presence:
                    continue
                else:
                    obj.present = presence
                    obj.save()
            else:
                obj = StudentPrecense(student=student, present=presence, class_lesson=current_class, date=datetime.date.today())
                obj.save()
        return HttpResponse('ok')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'main/login.htm')
    else:
        user = authenticate(request, password=request.POST['password'], username=request.POST['username'])
        if user:
            login(request, user)
            return redirect("/")
