from django.urls import path
from . import views


from django.urls import path
from .views import StartApplicationAPI

urlpatterns = [
    path('/start_application/', StartApplicationAPI.as_view(), name='start-application'),
    path('/add_courses/', StartApplicationAPI.as_view(), name='add_courses'),
]

