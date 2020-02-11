from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User

class_names = ['seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth']


class Field(models.Model):
    name = models.CharField(max_length=20)


class Grade(models.Model):
    display_name = models.CharField(max_length=20)
    grade = models.IntegerField(choices=list(zip(range(7, 13), class_names)))

    class Meta:
        verbose_name = 'grade'
        verbose_name_plural = 'grades'


class Class(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'class'
        verbose_name_plural = 'classes'


class Subject(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    fields = models.ManyToManyField(Field)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject)
    profile_photo = models.ImageField(upload_to='profile_photos/teachers/')


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reference_class = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="class")
    profile_photo = models.ImageField(upload_to='profile_photos/students/')


class ClassLesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    reference_class = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='class')
    start_datetime = models.DateTimeField()
    duration = models.DurationField(default=timedelta(hours=1, minutes=30))
