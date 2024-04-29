import datetime
from rest_framework import viewsets

from users.models import *
from student.utils import *
from student.seralizers import *
from users.pagination import CustomPagination

from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Q

import json
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view): # type: ignore
        return Admin.objects.filter(user=request.user).exists()
    
class IsAdminOrFacultyUser(permissions.BasePermission):
    def has_permission(self, request, view): # type: ignore
        return Admin.objects.filter(user=request.user).exists() or Faculty.objects.filter(user=request.user).exists() 

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
        only_new_students = str2bool(self.request.query_params.get('only_new_students', False)) # type: ignore
        only_final_approval = str2bool(self.request.query_params.get('only_final_approval', False)) # type: ignore
        only_in_progress = str2bool(self.request.query_params.get('only_in_progress', False)) # type: ignore

        if only_new_students:
            students = Student.objects.filter(ixo_details__isnull=True).filter(aus_id__isnull=False)
        elif only_final_approval:
            students = Student.objects.filter(submitted_form=True).filter(ixo_details__ixo_approval__isnull=True)
            # ensure that the student has been approved by the advisor and associate dean
            students = students.exclude(ixo_details__advisor_approval__isnull=False).filter(ixo_details__associate_dean_approval__isnull=False)
        elif only_in_progress:
            students = Student.objects.filter(ixo_details__isnull=False)
        else:
            students = Student.objects.all()
        students = student_search(self.request, students)
        students = filter_student_by_id(self.request, students)
        return students
    
class InitialApproval(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    def post(self, request):
        data = json.loads(request.body)
        student = Student.objects.get(id=data['id'])

        ixo_details = IXODetails.objects.create(
            moe_approval=str2bool(data['moeApproval']),
            usdoe_approval=str2bool(data['usdoeApproval']),
            acreditted=str2bool(data['acreditted']),
            acreditted_comments=data['acredittedComments'],
            agreement=str2bool(data['agreement']),
            initial_approval_date= datetime.datetime.now(),
        )
        student.ixo_details = ixo_details
        student.save()
        return JsonResponse({'message': 'Initial approval saved successfully'}, safe=False)
    
class FinalApproval(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    def post(self, request):
        data = json.loads(request.body)
        student = Student.objects.get(id=data['id'])
        if student.ixo_details is None:
            return JsonResponse({'message': 'Initial approval not found'}, safe=False)
        student.ixo_details.student_type = data['studentType'] 
        student.ixo_details.ixo_approval = str2bool(data['finalApproval'])
        student.ixo_details.ixo_approval_date = datetime.datetime.now()
        student.ixo_details.save()
        return JsonResponse({'message': 'Final approval saved successfully'}, safe=False)
    
class CoursesList(APIView):
    permission_classes = [IsAdminOrFacultyUser, IsAuthenticated]
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
    
    students = students.filter(id=id)
    
    return students

def get_student_by_id(request):
    id = request.query_params.get('id', None) # type: ignore
    student = Student.objects.filter(id=id).first()
    return student