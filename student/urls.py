from django.urls import path
from student.views import TestGet

urlpatterns = [
    path("test/", TestGet.as_view({'get': 'list'}),),
]