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
from django.views.decorators.csrf import csrf_exempt
import json

class StartApplicationAPI(APIView):
    @csrf_exempt  # This decorator is to allow POST requests without CSRF token for testing
    def add_student(request):
        if request.method == 'POST':
            # Load the data from the request body
            data = json.loads(request.body)
            
            # Create a new Student instance
            new_student = Student(
                student_id=data['id'],
                name=data['Name'],
                present_college=data['Present College'],
                present_major=data['Major'],
                current_standing=data['Current Standing'],
                mobile_number=data['Phone Number'],
                expected_graduation=data['Expected Graduation']
            )
            
            new_student.save()
            
            return JsonResponse({"message": "Student added successfully"}, status=201)
        else:
            return JsonResponse({"error": "Method not allowed"}, status=405)





