from rest_framework import viewsets

from users.models import *
from student.utils import *
from student.seralizers import *
from users.pagination import CustomPagination

from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Q

from student.utils import get_user_from_token
from users.views import do_comparison_on_application
import json
from threading import Thread
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view): # type: ignore
        return Admin.objects.filter(user=request.user).exists()

class FacultyList(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    def get(self, request):
        faculty = Faculty.objects.all()
        serializer = FacultySerializer(faculty, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request):
        data = json.loads(request.body)
        faculty = Faculty.objects.get(id=int(data['id']))
        if data.get('department') != None and data.get('department') != '':
            faculty.department = data['department']
        if data.get('faculty_type') != None and data.get('faculty_type') != '':
            faculty.faculty_type = data['faculty_type']
        
        faculty.save()
        return JsonResponse({'message': 'Faculty updated successfully'}, safe=False)