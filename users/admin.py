from django.contrib import admin
from .models import Faculty, University, Student, CourseApplication

admin.site.register(Faculty)
admin.site.register(University)
admin.site.register(Student)
admin.site.register(CourseApplication)
