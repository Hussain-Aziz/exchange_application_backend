from os import name
from django.db import models
from django.contrib.auth.models import User

FACULTY_CHOICES = (
    (0, 'Admin_Assistant'),
    (1, 'Teaching_Faculty'),
    (2, 'Head_of_Department'),
    (3, 'Advisor'),
    (4, 'Associate_Dean'),
    (5, 'Scholarship'),
    (6, 'Sponsorship'),
    (7, 'IXO'),
)

DEPARTMENTS = (
    (0, "Architecture"),
    (1, "Art and Design"),
    (2, "Arabic and Translation Studies"),
    (3, "Biology, Chemistry and Environmental Sciences"),
    (4, "English"),
    (5, "International Studies"),
    (6, "Media Communication"),
    (7, "Mathematics and Statistics"),
    (8, "Physics"),
    (9, "Psychology"),
    (10, "Chemical and Biological Engineering"),
    (11, "Civil Engineering"),
    (12, "Computer Science and Engineering"),
    (13, "Electrical Engineering"),
    (14, "Industrial Engineering"),
    (15, "Mechanical Engineering"),
    (16, "Accounting"),
    (17, "Economics"),
    (18, "Finance"),
    (19, "Management, Strategy and Entrepreneurship"),
    (20, "Marketing and Information Systems"),
)

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.PositiveIntegerField(choices=DEPARTMENTS, default=0)
    faculty_type = models.PositiveIntegerField(choices=FACULTY_CHOICES, default=0)    

class University(models.Model):
    university_id = models.AutoField(primary_key=True)
    university_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.university_name
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aus_id = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True, blank=True)
    phone_num = models.CharField(max_length=15, null=True, blank=True)
    expected_graduation = models.CharField(max_length=50, null=True, blank=True)
    present_college = models.CharField(max_length=50, null=True, blank=True)
    present_major = models.CharField(max_length=50, null=True, blank=True)
    current_standing = models.CharField(max_length=50, null=True, blank=True)
    host_contact_name = models.CharField(max_length=50, null=True, blank=True)
    host_contact_email = models.EmailField(max_length=50, null=True, blank=True)

class CourseApplication(models.Model):
    course_application_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    course_code = models.CharField(max_length=50, blank=True)
    course_title = models.CharField(max_length=50, blank=True)
    course_credits = models.IntegerField(default=0)
    aus_course = models.CharField(max_length=50, blank=True)
    syllabus = models.CharField(max_length=50, blank=True)
    aus_syllabus = models.CharField(max_length=50, blank=True)
    program_area = models.CharField(max_length=50, blank=True)
    grade_required = models.CharField(max_length=50, blank=True)
    pre_requisites_met = models.BooleanField(default=False)
    approved_status = models.BooleanField(default=False)