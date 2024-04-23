from django.urls import path
from .views import *

urlpatterns = [
    # get request to get list of faculty and their department post request to edit them
    path('faculty/', FacultyList.as_view(), name='faculty'),
]