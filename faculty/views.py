from rest_framework import viewsets

from users.models import *
from student.seralizers import *
from users.pagination import CustomPagination

from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Q

from student.utils import get_user_from_token
import json

class AvailableSyllabus(viewsets.ReadOnlyModelViewSet):
    pagination_class = CustomPagination
    serializer_class = CourseApplicationSerializer
    def get_queryset(self): # type: ignore
        faculty = get_faculty(self.request)

        courses = CourseApplication.objects.filter(department=faculty.department).filter(aus_syllabus__isnull=True) # if aus syllabus is null then it needs to be uploaded
        courses = course_search(self.request, courses)
        courses = get_course_by_id(self.request, courses)

        return courses
    
class UploadSyllabus(APIView):
    def post(self, request):
        data = json.loads(request.body)
        
        course_application = CourseApplication.objects.filter(course_application_id=data['id']).first()
        if course_application is None:
            return JsonResponse({"message": "Course not found"}, status=404)
        
        course_application.aus_syllabus = data['syllabus']
        course_application.save()
        
        return JsonResponse({"message": "Syllabus uploaded successfully"}, status=201)
    
    
class ApproveCourse(APIView):
    def post(self, request):
        data = json.loads(request.body)
        
        course_application = CourseApplication.objects.filter(course_application_id=data['id']).first()
        if course_application is None:
            return JsonResponse({"message": "Course not found"}, status=404)
        
        course_application.program_area = data['programArea']
        course_application.grade_required = data['gradeRequirement']
        course_application.pre_requisites_met = data['preReqsMet']
        course_application.approved_status = data['approved']
        course_application.save()
        
        return JsonResponse({"message": "Syllabus uploaded successfully"}, status=201)
        
class AvailableApprovals(viewsets.ReadOnlyModelViewSet):
    pagination_class = CustomPagination
    serializer_class = CourseApplicationSerializer
    def get_queryset(self): # type: ignore
        faculty = get_faculty(self.request)
        
        courses = CourseApplication.objects.filter(department=faculty.department).filter(aus_syllabus__isnull=False)
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