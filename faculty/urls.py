from django.urls import path
from .views import *

urlpatterns = [
    path('available_syllabus/', AvailableSyllabus.as_view({'get': 'list'}), name='available_syllabus'),
    path('available_approvals/', AvailableApprovals.as_view({'get': 'list'}), name='available_approvals'),
    path('upload_syllabus/', UploadSyllabus.as_view(), name='upload_syllabus'),
    path('approve_course/', ApproveCourse.as_view(), name='approve_course'),
]