from rest_framework import viewsets

import faculty
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

class IsFacultyUser(permissions.BasePermission):
    def has_permission(self, request, view): # type: ignore
        return Faculty.objects.filter(user=request.user).exists()

class AvailableSyllabus(viewsets.ReadOnlyModelViewSet):
    pagination_class = CustomPagination
    serializer_class = CourseApplicationSerializer
    permission_classes = [IsFacultyUser, IsAuthenticated]
    def get_queryset(self): # type: ignore
        faculty = get_faculty(self.request)

        courses = CourseApplication.objects.filter(department=faculty.department).filter(aus_syllabus__isnull=True) # if aus syllabus is null then it needs to be uploaded
        courses = course_search(self.request, courses)
        courses = get_course_by_id(self.request, courses)

        return courses
    
class UploadSyllabus(APIView):
    permission_classes = [IsFacultyUser, IsAuthenticated]
    def post(self, request):
        data = json.loads(request.body)
        
        course_application = CourseApplication.objects.filter(course_application_id=int(data['id'])).first()
        if course_application is None:
            return JsonResponse({"message": "Course not found"}, status=404)
        
        course_application.aus_syllabus = data['syllabus']
        course_application.save()

        # fire and forget
        Thread(target=do_comparison_on_application, args=(course_application,)).start()
        
        return JsonResponse({"message": "Syllabus uploaded successfully"}, status=201)
    
    
class ApproveCourse(APIView):
    permission_classes = [IsFacultyUser, IsAuthenticated]
    def post(self, request):
        faculty = get_faculty(request)
        data = json.loads(request.body)
        
        course_application = CourseApplication.objects.filter(course_application_id=int(data['id'])).first()
        if course_application is None:
            return JsonResponse({"message": "Course not found"}, status=404)
        
        if data.get('programArea') != None and data.get('programArea') != '':
            course_application.program_area = data['programArea']
        if data.get('gradeRequirement') != None and data.get('gradeRequirement') != '':
            course_application.grade_required = data['gradeRequirement']
        if data.get('preReqsMet') != None and data.get('preReqsMet') != '':
            course_application.pre_requisites_met = str2bool(data['preReqsMet'])
        if data.get('approved') != None and data.get('approved') != '':
            if faculty.faculty_type == 0 or faculty.faculty_type == 2:
                course_application.approved_status = str2bool(data['approved'])
            else:
                course_application.delegated_approval = str2bool(data['approved'])
        if data.get('delegate') != None and data.get('delegate') != '':
            faculty = Faculty.objects.filter(user__username=data['delegate']).first()
            if faculty is None:
                return JsonResponse({"message": "Faculty not found"}, status=404)
            course_application.delegated_to = faculty
        course_application.save()
        
        return JsonResponse({"message": "Syllabus uploaded successfully"}, status=201)
        
class AvailableApprovals(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsFacultyUser, IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = CourseApplicationSerializer
    def get_queryset(self): # type: ignore
        faculty = get_faculty(self.request)
        
        courses = CourseApplication.objects.filter(department=faculty.department)
        courses = courses.filter(aus_syllabus__isnull=False)
        courses = courses.filter(approved_status__isnull=True)

        if faculty.faculty_type == 1 or faculty.faculty_type == 3 or faculty.faculty_type == 4:
            courses = courses.filter(Q(delegated_to=faculty) & Q(delegated_approval__isnull=True))
        if faculty.faculty_type == 0 or faculty.faculty_type == 2:
            courses = courses.filter(
                Q(delegated_to__isnull=True) # not delegated
                | Q(delegated_to=faculty) # delegated to target
                | Q(delegated_to__isnull=False) & Q(delegated_approval__isnull=False) # delegated and approved
                )

        courses = course_search(self.request, courses)
        courses = get_course_by_id(self.request, courses)
            
        return courses
    

def get_faculty(request):
    user = get_user_from_token(request)
    faculty = Faculty.objects.filter(user=user).first()
    if faculty is None:
        raise Exception("Faculty not found")
    return faculty

def course_search(request, courses):
    search_text = request.query_params.get('search_text', None) # type: ignore

    if search_text is None or search_text == '':
        return courses
    
    return courses.filter(
        Q(student__aus_id__icontains=search_text) |
        Q(student__name__icontains=search_text) |
        Q(course_code__icontains=search_text) |
        Q(course_title__icontains=search_text)
    )

def get_course_by_id(request, courses):
    course_application_id = request.query_params.get('id', None) # type: ignore

    if course_application_id is None:
        return courses
    
    return courses.filter(course_application_id=course_application_id)