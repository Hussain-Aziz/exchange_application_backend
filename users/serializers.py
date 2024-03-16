from rest_framework import serializers
from .models import Student

class StudentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  # List all the fields of your model here.
