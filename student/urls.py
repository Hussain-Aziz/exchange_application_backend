from django.urls import path
from . import views


from django.urls import path
from .views import StartApplicationAPI, AddCourseAPI, ApplicationInfoAPI

urlpatterns = [
    # post endpoint to start student application (body: id, name, university, mobileNumber, expectedGraduation, presentCollege, presentMajor, currentStanding, hostContactName, hostContactEmail)
    path('start_application/', StartApplicationAPI.as_view(), name='start_application'),
    # get endpoint to get student application info
    path('application_info/', ApplicationInfoAPI.as_view(), name='application_info'),
    # post endpoint to add course to their application (body: course_name, course_code, course_credits, course_semester, course_year)
    # get endpoint to get list of courses in their application
    path('courses/', AddCourseAPI.as_view(), name='courses'),
]

