from exchange_application.settings import EMAIL_HOST_USER
from users.models import *
from student.seralizers import *
from rest_framework.views import APIView
from users.models import Student
from django.http import JsonResponse
from django.core.mail import send_mail

from .utils import get_user_from_token, str2bool
import json
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from users.models import COLLEGES

class IsStudentUser(permissions.BasePermission):
    def has_permission(self, request, view): # type: ignore
        return Student.objects.filter(user=request.user).exists()

class StartApplicationAPI(APIView):
    permission_classes = [IsAuthenticated, IsStudentUser]
    def post(self, request):
        # Load the data from the request body
        data = json.loads(request.body)

        user = get_user_from_token(request)
        
        university = University.objects.filter(university_name=data['university']).first()
        if university is None:
            university = University.objects.create(university_name=data['university'])

        college_dict = dict((y, x) for x, y in COLLEGES)
        
        student = Student.objects.filter(user=user).first()
        if student is None:
            return JsonResponse({"message": "Student doesn't exists"}, status=400)
        student.aus_id = data['id']
        student.name =  data['name']
        student.university = university
        student.phone_num = data['mobileNumber']
        student.expected_graduation =  data['expectedGraduation']
        student.present_college =  college_dict[data['presentCollege']]
        student.present_major =  data['presentMajor']
        student.current_standing =  data['currentStanding']
        student.host_contact_name =  data['hostContactName']
        student.host_contact_email =  data['hostContactEmail']
        student.department = data['department']
        student.save()
        
        return JsonResponse({"message": "Student added successfully"}, status=200)
    
    def delete(self, request):
        user = get_user_from_token(request)
        student = Student.objects.filter(user=user).first()
        if student is None:
            return JsonResponse({"message": "Student not found"}, status=404)
        
        # delete student courses
        courses = CourseApplication.objects.filter(student=student)
        for course in courses:
            course.delete()

        student.aus_id = None
        student.name = None
        student.university = None
        student.phone_num = None
        student.expected_graduation = None
        student.present_college = None
        student.present_major = None
        student.department = None
        student.current_standing = None
        student.host_contact_name = None
        student.host_contact_email = None
        student.ixo_details = None
        student.submitted_form = False
        student.form_comments = None

        student.save()
        
        return JsonResponse({"message": "Student deleted successfully"}, status=204)
    
class ApplicationInfoAPI(APIView):
    permission_classes = [IsAuthenticated, IsStudentUser]
    def get(self, request):
        user = get_user_from_token(request)
        student = Student.objects.filter(user=user).first()
        if student is None:
            return JsonResponse({"message": "Student not found"}, status=404)
        
        serializer = StudentApplicationSerializer(student)
        return JsonResponse(serializer.data, safe=False)


class AddCourseAPI(APIView):
    permission_classes = [IsAuthenticated, IsStudentUser]
    def post(self, request):
        # Load the data from the request body
        data = json.loads(request.body)

        # get token from header
        user = get_user_from_token(request)


        student = Student.objects.filter(user=user).first()
        if student is None:
            return JsonResponse({"message": "Student not found"}, status=404)
        
        aus_course = data['ausCourse']
        course_subject = aus_course.split(" ")[0]

        try:
            department = course_to_deparment[course_subject]
        except:
            department = 0
    
        # Create a new Course instance
        new_course = CourseApplication(
            student = student,
            university = student.university,
            course_code = data['hostCourseCode'],
            course_title = data['hostCouseTitle'],
            course_credits = int(data['courseCredits']),
            aus_course = data['ausCourse'],
            syllabus = data['hostUniversitySyllabus'],
            department = department,
        )

        if data.get('ausSyllabus') != None and data.get('ausSyllabus') != '':
            new_course.aus_syllabus = data['ausSyllabus']
        new_course.save()

        hod = Faculty.objects.filter(department=department).filter(faculty_type=2).first()
        aa = Faculty.objects.filter(department=department).filter(faculty_type=0).first()
        if hod is not None and aa is not None:
            send_mail("Course Approval", 
                      f"New course approval request has been made. Please approve it at https://ausxchange.com/faculty/course_requests/{new_course.course_application_id}", 
                      EMAIL_HOST_USER, 
                      [hod.user.username, aa.user.username])
        
        return JsonResponse({"message": "Course added successfully", "id": new_course.course_application_id}, status=200)

    def get(self, request):
        user = get_user_from_token(request)
        student = Student.objects.filter(user=user).first()
        courses = CourseApplication.objects.filter(student=student)
        serializer = CourseApplicationSerializer(courses, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def delete(self, request):
        data = json.loads(request.body)
        
        course_application = CourseApplication.objects.filter(course_application_id=int(data['id'])).first()
        if course_application is None:
            return JsonResponse({"message": "Course not found"}, status=404)
        
        course_application.delete()
        
        return JsonResponse({"message": "Course deleted successfully"}, status=204)


class SubmitApplication(APIView):
    permission_classes = [IsAuthenticated, IsStudentUser]
    def post(self, request):
        user = get_user_from_token(request)
        student = Student.objects.filter(user=user).first()
        if student is None or student.ixo_details is None:
            return JsonResponse({"message": "Student not found"}, status=404)
        
        student.submitted_form = True
        if request.data.get('scholarship') is not None:
            student.ixo_details.scholarship_approval = False
        if request.data.get('sponsorship') is not None:
            student.ixo_details.sponsorship_approval = False

        student.ixo_details.save()
        student.save()

        adean = Faculty.objects.filter(department=student.department).filter(faculty_type=4).first()
        advisor = Faculty.objects.filter(department=student.department).filter(faculty_type=3).first()

        if adean is not None and advisor is not None:
            send_mail("Application Submission", 
                      f"New application has been submitted. Please approve it at https://ausxchange.com/faculty/approve_application/{student.id}", 
                      EMAIL_HOST_USER, 
                      [adean.user.username, advisor.user.username])

        
        return JsonResponse({"message": "Application submitted successfully"}, status=200)

course_to_deparment = {
    "ABRD": 0,
    "ACC": 17,
    "ANT": 6,
    "ARA": 3,
    "ARC": 1,
    "ART": 2,
    "ASE": 0,
    "AUS": 0,
    "BIO": 4,
    "BIS": 20,
    "BLW": 20,
    "BME": 0,
    "BPE": 0,
    "BSE": 0,
    "BUS": 20,
    "CHE": 11,
    "CHM": 4,
    "CMP": 13,
    "CMT": 0,
    "COE": 13,
    "CVE": 12,
    "DES": 2,
    "DLDG": 0,
    "ECO": 18,
    "EGM": 0,
    "ELE": 14,
    "ELP": 0,
    "ELT": 5,
    "ENG": 5,
    "ENV": 4,
    "ESM": 15,
    "EWE": 0,
    "FIN": 19,
    "FLM": 2,
    "FRN": 0,
    "GEO": 6,
    "GMPA": 0,
    "HIS": 6,
    "IDE": 1,
    "IDS": 0,
    "IEN": 0,
    "INE": 15,
    "INS": 15,
    "ISA": 21,
    "KOR": 0,
    "MBA": 0,
    "MCE": 16,
    "MCM": 7,
    "MGT": 20,
    "MKT": 21,
    "MSE": 0,
    "MTH": 8,
    "MTR": 0,
    "MUM": 2,
    "MUS": 7, # check
    "NGN": 0,
    "PHI": 6,
    "PHY": 9,
    "POL": 6,
    "PSY": 10,
    "QBA": 18,
    "SCM": 21,
    "SOC": 6,
    "STA": 8,
    "THE": 7, # check
    "TRA": 3,
    "UPA": 0,
    "UPL": 1,
    "VIS": 2,
    "WRI": 5,
    "WST": 0,
}

department_to_college = {
    1: "CAAD",
    2: "CAAD",
    3: "CAS",
    4: "CAS",
    5: "CAS",
    6: "CAS",
    7: "CAS",
    8: "CAS",
    9: "CAS",
    10: "CAS",
    11: "CEN",
    12: "CEN",
    13: "CEN",
    14: "CEN",
    15: "CEN",
    16: "CEN",
    17: "SBA",
    18: "SBA",
    19: "SBA",
    20: "SBA",
    21: "SBA",
}
