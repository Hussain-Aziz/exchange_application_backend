from django.urls import path
from . import views


from django.urls import path
from .views import StartApplicationAPI

urlpatterns = [
    path('start-application/', StartApplicationAPI.as_view(), name='start-application'),
]

