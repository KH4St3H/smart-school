from django.shortcuts import render
from attendance.models import StudentPresence


def show_absents(request):
    return render(request, 'management/base.htm')
