from rest_framework import serializers
from exchange_application.views import UserSerializer
from users.models import *

class StudentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  

class FacultySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Faculty
        fields = '__all__'

class CourseApplicationSerializer(serializers.ModelSerializer):
    student = StudentApplicationSerializer()
    delegated_to = FacultySerializer()
    class Meta:
        model = CourseApplication
        fields = '__all__'

