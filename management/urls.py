from django.urls import path
from . import views

urlpatterns = [
    path('attendance/', views.show_absents, name='show-absents')
]
app_name = 'management'
