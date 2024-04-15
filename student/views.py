from rest_framework import viewsets

from users.models import *
from student.models import *
from student.seralizers import *
from users.pagination import CustomPagination

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import Student
from django.http import JsonResponse

from .utils import get_user_from_token
import json

class StartApplicationAPI(APIView):
    def post(self, request):
        # Load the data from the request body
        data = json.loads(request.body)

        user = get_user_from_token(request)
        
        university = University.objects.filter(university_name=data['university']).first()
        if university is None:
            university = University.objects.create(university_name=data['university'])
        
        student = Student.objects.filter(user=user).first()
        if student is None:
            return JsonResponse({"message": "Student already exists"}, status=400)
        student.aus_id = data['id']
        student.name =  data['name']
        student.university = university
        student.phone_num = data['mobileNumber']
        student.expected_graduation =  data['expectedGraduation']
        student.present_college =  data['presentCollege']
        student.present_major =  data['presentMajor']
        student.current_standing =  data['currentStanding']
        student.host_contact_name =  data['hostContactName']
        student.host_contact_email =  data['hostContactEmail']
        student.save()
        
        return JsonResponse({"message": "Student added successfully"}, status=201)
    
class ApplicationInfoAPI(APIView):
    def get(self, request):
        user = get_user_from_token(request)
        student = Student.objects.filter(user=user).first()
        if student is None:
            return JsonResponse({"message": "Student not found"}, status=404)
        
        serializer = StudentApplicationSerializer(student)
        return JsonResponse(serializer.data, safe=False)


class AddCourseAPI(APIView):
    def post(self, request):
        # Load the data from the request body
        data = json.loads(request.body)

        # get token from header
        user = get_user_from_token(request)


        student = Student.objects.filter(user=user).first()
        if student is None:
            return JsonResponse({"message": "Student not found"}, status=404)
    
        # Create a new Course instance
        new_course = CourseApplication(
            student = student,
            university = student.university,
            course_code = data['hostCourseCode'],
            course_title = data['hostCouseTitle'],
            course_credits = int(data['courseCredits']),
            aus_course = data['ausCourse'],
            syllabus = data['hostUniversitySyllabus'],
        )
        new_course.save()
        
        return JsonResponse({"message": "Course added successfully"}, status=201)

    def get(self, request):
        user = get_user_from_token(request)
        student = Student.objects.filter(user=user).first()
        courses = CourseApplication.objects.filter(student=student)
        serializer = CourseApplicationSerializer(courses, many=True)
        return JsonResponse(serializer.data, safe=False)



