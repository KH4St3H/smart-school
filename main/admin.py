from django.contrib import admin
from .models import Field, Grade, Class, Subject, Teacher, Student, ClassLesson, Lesson, TimeTable

for model in [Field, Grade, Class, Student, Subject, Teacher, ClassLesson, Lesson, TimeTable]:
    admin.site.register(model)
