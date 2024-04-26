from rest_framework import serializers
from exchange_application.views import UserSerializer
from users.models import *

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'

class IXODetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IXODetails
        fields = '__all__'

class StudentApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    university = UniversitySerializer()
    ixo_details = IXODetails()
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

