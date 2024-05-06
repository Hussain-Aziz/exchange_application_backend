import datetime
from rest_framework import viewsets

from admin.views import filter_student_by_id, get_student_by_id, student_search
from django.core.mail import send_mail
from exchange_application.settings import EMAIL_HOST_USER
from users.models import *
from student.utils import *
from student.seralizers import *
from users.pagination import CustomPagination

from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Q

from student.utils import get_user_from_token
import json
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
        
        # if aus syllabus is null then it needs to be uploaded
        courses = CourseApplication.objects.filter(Q(department=faculty.department) & Q(aus_syllabus__isnull=True) & Q(ignore_aus_syllabus=False))
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
        
        if data.get('ignore_aus_syllabus') != None and data.get('ignore_aus_syllabus') != '':
            course_application.ignore_aus_syllabus = str2bool(data['ignore_aus_syllabus'])
            course_application.save()
            return JsonResponse({"message": "Syllabus ignored successfully"}, status=200)
        else:
            course_application.aus_syllabus = data['syllabus']
            course_application.save()
            return JsonResponse({"message": "Syllabus uploaded successfully", 'id': course_application.course_application_id}, status=200)
    
    
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
            if faculty.faculty_type == 0 or faculty.faculty_type == 2 or course_application.force_approval_to == faculty.user.username:
                course_application.approved_status = str2bool(data['approved'])
            else:
                course_application.delegated_approval = str2bool(data['approved'])
        if data.get('comments') != None and data.get('comments') != '':
            course_application.comments = data['comments']
        if data.get('delegate') != None and data.get('delegate') != '':
            course_application.delegated_to = data['delegate']
        course_application.save()

        if course_application.approved_status:
            send_mail("Course Approved", f"Your course {course_application.course_code} has been approved by {faculty.user.username}", EMAIL_HOST_USER, [course_application.student.user.username])
            if course_application.force_approval_to is not None:
                course_application.approved_by = course_application.force_approval_to
                course_application.save()
            elif faculty.faculty_type == 2:
                course_application.approved_by = faculty.user.username
                course_application.save()
            else:
                hod = Faculty.objects.filter(department=faculty.department, faculty_type=2).first()
                if hod is not None:
                    course_application.approved_by = hod.user.username
                    course_application.save()
        
        
        return JsonResponse({"message": "Syllabus uploaded successfully"}, status=200)
        
class AvailableApprovals(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsFacultyUser, IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = CourseApplicationSerializer
    def get_queryset(self): # type: ignore
        faculty = get_faculty(self.request)
        
        courses = CourseApplication.objects.all()

        courses = courses.filter(Q(aus_syllabus__isnull=False) | Q(ignore_aus_syllabus=True)) # remove courses that dont have syllabus yet
        courses = courses.filter(approved_status__isnull=True) # remove courses that are already approved

        if faculty.faculty_type == 1 or faculty.faculty_type == 3 or faculty.faculty_type == 4: # tf, advisor, associate dean
            courses = courses.filter(
                (Q(delegated_to=faculty.user.username) & Q(delegated_approval__isnull=True)) # delegated to but not suggested yet
                | Q(force_approval_to=faculty.user.username) # force approval target
                )
        if faculty.faculty_type == 0 or faculty.faculty_type == 2: # aa, hod
            courses = courses.filter(
                (Q(delegated_to__isnull=True) & Q(department=faculty.department)) # hod/aa of department and its not delegated
                | (Q(delegated_to=faculty.user.username) | Q(force_approval_to=faculty.user.username)) # delegated or force approval target
                | (Q(delegated_to__isnull=False) & Q(delegated_approval__isnull=False) & Q(department=faculty.department)) # delegated and suggestion given and same department
                )

        courses = course_search(self.request, courses)
        courses = get_course_by_id(self.request, courses)
            
        return courses
    
class StudentList(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsFacultyUser, IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = StudentApplicationSerializer
    
    def get_queryset(self): # type: ignore
        faculty = get_faculty(self.request)

        students = Student.objects.all()

        if faculty.faculty_type == 3:
            students = Student.objects.filter(department=faculty.department).filter(submitted_form=True).filter(ixo_details__advisor_approval__isnull=True)
        if faculty.faculty_type == 4:
            students = Student.objects.filter(present_college=faculty.college).filter(submitted_form=True).filter(ixo_details__associate_dean_approval__isnull=True)
        if faculty.faculty_type == 5:
            students = Student.objects.filter(submitted_form=True).filter(ixo_details__scholarship_approval__isnull=True)
        if faculty.faculty_type == 6:
            students = Student.objects.filter(submitted_form=True).filter(ixo_details__sponsorship_approval__isnull=True)

        students = student_search(self.request, students)
        students = filter_student_by_id(self.request, students)
        return students

class ApproveStudent(APIView):
    def post(self, request):
        faculty = get_faculty(request)
        data = json.loads(request.body)
        
        student = Student.objects.filter(id=int(data['id'])).first()
        if student is None:
            return JsonResponse({"message": "Student not found"}, status=404)
        
        if student.ixo_details is None:
            return JsonResponse({"message": "Student application not submitted"}, status=400)
        
        if (str2bool(data['approved']) == False):
            # force reject all
            student.ixo_details.advisor_approval = None
            student.ixo_details.associate_dean_approval = None
            student.ixo_details.scholarship_approval = None
            student.ixo_details.sponsorship_approval = None
            student.submitted_form = False
            student.form_comments = data['comments']
            student.ixo_details.save()
            student.save()
            send_mail("Application Rejected", f"Your application has been rejected because {student.form_comments}", EMAIL_HOST_USER, [student.user.username])
            return JsonResponse({"message": "Student rejected successfully"}, status=200)

        
        if faculty.faculty_type == 3:
            student.ixo_details.advisor_approval = str2bool(data['approved'])
            student.ixo_details.advisor_approval_date = datetime.datetime.now()
        if faculty.faculty_type == 4:
            student.ixo_details.associate_dean_approval = str2bool(data['approved'])
            student.ixo_details.associate_dean_approval_date = datetime.datetime.now()
        if faculty.faculty_type == 5:
            student.ixo_details.scholarship_approval = str2bool(data['approved'])
            student.ixo_details.scholarship_approval_date = datetime.datetime.now()
        if faculty.faculty_type == 6:
            student.ixo_details.sponsorship_approval = str2bool(data['approved'])
            student.ixo_details.sponsorship_approval_date = datetime.datetime.now()
        
        student.ixo_details.save()
        
        return JsonResponse({"message": "Student approved successfully"}, status=200)
    

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