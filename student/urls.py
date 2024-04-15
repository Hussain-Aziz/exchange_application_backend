from django.urls import path
from . import views


from django.urls import path
from .views import StartApplicationAPI, AddCourseAPI, ApplicationInfoAPI

urlpatterns = [
    path('start_application/', StartApplicationAPI.as_view(), name='start-application'),
    path('application_info/', ApplicationInfoAPI.as_view(), name='application-info'),
    path('courses/', AddCourseAPI.as_view(), name='courses'),
]

