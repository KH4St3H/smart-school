from django.test import TestCase
from .models import Field, Grade, Class, Subject, Teacher, Student, ClassLesson, Lesson, User
from PIL import Image


class MainTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(first_name="Hojat", last_name='Kamali',
                                        username='hkamali', password="nvraeiygvawe")

        field = Field.objects.create(name="Mathematics and Physics")
        grade = Grade.objects.create(display_name="10th", grade=10)
        c = Class.objects.create(grade=grade, name='103', field=field)
        subject = Subject.objects.create(name='Math')
        Lesson.objects.create(subject=subject, grade=grade)

        teacher = Teacher.objects.create(user=user, subject=subject,
                                         profile_photo=Image.open('~/Pictures/profile_photo_default.jpeg'))

        student_user = User.objects.create_user(first_name="Ali Asghar", last_name='Bahmaniar',
                                                username='alibahman', password="igvjrdao2arij")

        student = Student.objects.create(user=user, reference_class=c,
                                         profile_photo=Image.open('~/Downloads/photo_2020-01-25_21-23-09.jpg'))
