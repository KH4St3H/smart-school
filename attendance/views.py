from django.shortcuts import render, HttpResponse, Http404
from django.contrib.auth.views import login_required

from .models import StudentPresence
from main.models import Teacher

import datetime


def teacher_only(func):
    def wrapper(request):
        user = request.user
        if Teacher.objects.filter(user=user):
            return func(request)
        return Http404()
    return wrapper


@login_required
@teacher_only
def attendance(request):
    current_class = request.user.teacher.has_class()
    prev_attendance = StudentPresence.objects.filter(class_lesson=current_class, date=datetime.date.today())
    if request.method == 'GET':
        if current_class:
            if prev_attendance:
                states = prev_attendance
            else:
                prev_class = current_class.has_previous_class()
                if prev_class:
                    attendance_list = StudentPresence.objects.filter(class_lesson=prev_class[0],
                                                                     date=datetime.date.today())
                    if attendance_list:
                        states = attendance_list
                    else:
                        states = False
                else:
                    states = False
            return render(request, 'attendance/attendance.htm', {'class': current_class.related_class, 'states': states})
        else:
            return render(request, 'attendance/attendance.htm', {'class': False, 'states': False})

    elif request.method == 'POST':
        i = 0
        for student in current_class.related_class.student_set.all():
            presence = True if request.POST.getlist('states[]')[i] == 'true' else False
            i += 1
            if prev_attendance:
                obj = prev_attendance.filter(student=student)[0]
                if obj.present == presence:
                    continue
                else:
                    obj.present = presence
                    obj.save()
            else:
                obj = StudentPresence(student=student, present=presence, class_lesson=current_class,
                                      date=datetime.date.today())
                obj.save()
        return HttpResponse('ok')
