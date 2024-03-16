from django.urls import path
from . import views


from django.urls import path
from .views import StartApplicationAPI

urlpatterns = [
    path('http://localhost:3000/student/start_application/', StartApplicationAPI.as_view(), name='start-application'),
    path('http://localhost:3000/student/add_courses/', StartApplicationAPI.as_view(), name='add_courses'),
     path('http://localhost:3000/login/register/', StartApplicationAPI.as_view(), name='register'),

]

