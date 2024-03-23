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
from users.serializers import StudentApplicationSerializer
from rest_framework.decorators import api_view

class StartApplicationAPI(APIView):
    def post(self, request, *args, **kwargs):
        print("request.data: ", request.data)
        serializer = StudentApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
@api_view(['POST'])
def add_student(request):
    if request.method == 'POST':
        serializer = StudentApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)