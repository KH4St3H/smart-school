from django.db import models
from datetime import timedelta, datetime
from django.contrib.auth.models import User

class_names = ['seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth']
weekdays = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday')
]


class Field(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Grade(models.Model):
    display_name = models.CharField(max_length=20)
    grade = models.IntegerField(choices=list(zip(range(7, 13), class_names)))

    class Meta:
        verbose_name = 'grade'
        verbose_name_plural = 'grades'

    def __str__(self):
        return self.display_name


class Class(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'class'
        verbose_name_plural = 'classes'

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    fields = models.ManyToManyField(Field)

    def __str__(self):
        return self.grade.display_name + ' ' + self.subject.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject)
    profile_photo = models.ImageField(upload_to='profile_photos/teachers/')

    class Meta:
        permissions = (
            ("add_post", "Can add posts"),
        )

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def has_class(self):
        weekday = datetime.now().weekday() + 1
        current = datetime.now().time()
        first = datetime.now() - timedelta(hours=1, minutes=30)
        first = first.time()
        print(weekday)
        print(current)
        print(first)
        timetable = TimeTable.objects.filter(weekday=weekday, start_time__range=(first, current))
        if timetable:
            timetable = timetable[0]
        else:
            return False
        _class = timetable.classlesson_set.filter(teacher=self)
        if _class:
            return _class[0].related_class
        return False


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reference_class = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="class")
    profile_photo = models.ImageField(upload_to='profile_photos/students/')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class TimeTable(models.Model):
    weekday = models.IntegerField(choices=weekdays)
    start_time = models.TimeField()

    def __str__(self):
        return dict(weekdays)[self.weekday] + ' - ' + self.start_time.strftime("%H:%M")


class ClassLesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    time = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    related_class = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.related_class.name + ' ' + self.lesson.subject.name
