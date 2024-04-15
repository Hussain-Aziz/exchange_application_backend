from rest_framework import serializers
from users.models import *

class StudentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  


class CourseApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseApplication
        fields = '__all__'