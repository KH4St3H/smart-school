from django.db import models
from main.models import Student, ClassLesson


class StudentPresence(models.Model):
    student = models.OneToOneField(Student, models.CASCADE)
    present = models.BooleanField(default=True)
    class_lesson = models.ForeignKey(ClassLesson, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
