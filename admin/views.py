from rest_framework import viewsets

from users.serializers import *
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
    
class StudentList(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser, IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = StudentApplicationSerializer
    
    def get_queryset(self): # type: ignore
        students = Student.objects.filter(aus_id__isnull=False)
        students = student_search(self.request, students)
        students = filter_student_by_id(self.request, students)
        return students
    
class CoursesList(APIView):
    def get(self, request):
        student = get_student_by_id(request)
        courses = CourseApplication.objects.filter(student=student)
        serializer = CourseApplicationSerializer(courses, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def patch(self, request):
        data = json.loads(request.body)
        course = CourseApplication.objects.get(course_application_id=int(data['id']))
        if data.get('assignedTo') != None and data.get('assignedTo') != '':
            course.force_approval_to = data['assignedTo']
            
        course.save()
        return JsonResponse({'message': 'Course updated successfully'}, safe=False)
    
class ForceApproval(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    def post(self, request):
        data = json.loads(request.body)
        course_application = CourseApplication.objects.filter(course_application_id=int(data['id'])).first()
        if course_application is None:
            return JsonResponse({"message": "Course not found"}, status=404)
        
        course_application.force_approval_to = data['email']
        course_application.save()
        return JsonResponse({"message": "Approval forced successfully"}, status=201)
    

def student_search(request, students):
    search_text = request.query_params.get('search_text', None) # type: ignore

    if search_text is None or search_text == '':
        return students
    
    students = students.filter(
        Q(user__username__icontains=search_text)
        | Q(aus_id__icontains=search_text)
        | Q(name__icontains=search_text)
        )
    
    return students

def filter_student_by_id(request, students):
    id = request.query_params.get('id', None) # type: ignore

    if id is None or id == '':
        return students
    
    print(id)
    
    students = students.filter(aus_id=id)
    
    return students

def get_student_by_id(request):
    id = request.query_params.get('id', None) # type: ignore
    student = Student.objects.filter(aus_id=id).first()
    return student