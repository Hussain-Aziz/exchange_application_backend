from django.urls import path
from .views import *

urlpatterns = [
    # get request to get list of faculty and their department post request to edit them
    path('faculty/', FacultyList.as_view(), name='faculty'),
    path('student/', StudentList.as_view({'get': 'list'}), name='student'),
    path('courses/', CoursesList.as_view(), name='courses'),
]