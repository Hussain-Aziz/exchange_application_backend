from django.urls import path
from .views import *

urlpatterns = [
    # get endpoint to get list of available syllabus, optional param for id to get specific course info
    path('available_syllabus/', AvailableSyllabus.as_view({'get': 'list'}), name='available_syllabus'),
    # get endpoint to get list of available approvals, optional param for id to get specific course info
    path('available_approvals/', AvailableApprovals.as_view({'get': 'list'}), name='available_approvals'),
    # post endpoint to upload syllabus (body: syllabus)
    path('upload_syllabus/', UploadSyllabus.as_view(), name='upload_syllabus'),
    # post endpoint to approve course (body: programArea, gradeRequirement, preReqsMet, approved)
    path('approve_course/', ApproveCourse.as_view(), name='approve_course'),
    path('approve_student/', ApproveStudent.as_view(), name='approve_student'),
    path('list_students/', StudentList.as_view({'get': 'list'}), name='list_students'),
]