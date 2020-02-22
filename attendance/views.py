from django.shortcuts import render, HttpResponse, Http404, HttpResponseRedirect, reverse
from django.contrib.auth.views import login_required

# rest test
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
# end rest test

from .models import StudentPresence
from main.models import Teacher, Student

import datetime


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        teacher = Teacher.objects.filter(user=request.user)
        if not teacher:
            return False
        return True


class CurrentClassStudentsList(APIView):
    def post(self, request, format=None):
        current_class = request.user.teacher.has_class()
        if not current_class:
            return Response(status=status.HTTP_204_NO_CONTENT)
        current_class_students = [i.user for i in Student.objects.filter(reference_class=current_class.related_class)]
        serializer = UserSerializer(current_class_students, many=True)
        return Response(serializer.data)


def teacher_only(func):
    def wrapper(request):
        user = request.user
        if Teacher.objects.filter(user=user):
            return func(request)
        elif request.user.is_superuser:   # redirecting to another function if the user is superuser or basically
            return view_absents(request)    # school staff, principle or etc.
        return Http404()
    return wrapper


@api_view(['POST'])
def current_class_students_list(request):
    tracher = Teacher.objects.get(user=request.user)
    current_class = Teacher.objects.get(user=request.user).has_class()
    if not current_class:
        return Response(status=status.HTTP_204_NO_CONTENT)
    current_class_students = Student.objects.filter(reference_class=current_class.related_class)
    serializer = UserSerializer(current_class_students, many=True)
    return Response(serializer.data)


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
            return render(request, 'attendance/attendance.htm', {'class': current_class.related_class,
                                                                 'states': states})
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


def view_absents(request):
    return HttpResponseRedirect(reverse('management:show-absents'))
