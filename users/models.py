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
    (0, "Unknown"),
    (1, "Architecture"),
    (2, "Art and Design"),
    (3, "Arabic and Translation Studies"),
    (4, "Biology, Chemistry and Environmental Sciences"),
    (5, "English"),
    (6, "International Studies"),
    (7, "Media Communication"),
    (8, "Mathematics and Statistics"),
    (9, "Physics"),
    (10, "Psychology"),
    (11, "Chemical and Biological Engineering"),
    (12, "Civil Engineering"),
    (13, "Computer Science and Engineering"),
    (14, "Electrical Engineering"),
    (15, "Industrial Engineering"),
    (16, "Mechanical Engineering"),
    (17, "Accounting"),
    (18, "Economics"),
    (19, "Finance"),
    (20, "Management, Strategy and Entrepreneurship"),
    (21, "Marketing and Information Systems"),
)

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.PositiveIntegerField(choices=DEPARTMENTS, default=0)
    faculty_type = models.PositiveIntegerField(choices=FACULTY_CHOICES, default=0)    

class University(models.Model):
    university_id = models.AutoField(primary_key=True)
    university_name = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.university_name
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aus_id = models.CharField(max_length=250, blank=True, null=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True, blank=True)
    phone_num = models.CharField(max_length=15, null=True, blank=True)
    expected_graduation = models.CharField(max_length=250, null=True, blank=True)
    present_college = models.CharField(max_length=250, null=True, blank=True)
    present_major = models.CharField(max_length=250, null=True, blank=True)
    current_standing = models.CharField(max_length=250, null=True, blank=True)
    host_contact_name = models.CharField(max_length=250, null=True, blank=True)
    host_contact_email = models.EmailField(max_length=250, null=True, blank=True)

class CourseApplication(models.Model):
    course_application_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    course_code = models.CharField(max_length=250, blank=True, null=True)
    course_title = models.CharField(max_length=250, blank=True, null=True)
    course_credits = models.IntegerField(default=0)
    aus_course = models.CharField(max_length=250, blank=True, null=True)
    department = models.IntegerField(choices=DEPARTMENTS, default=0, null=True)
    syllabus = models.CharField(max_length=250, blank=True, null=True)
    aus_syllabus = models.CharField(max_length=250, blank=True, null=True)
    program_area = models.CharField(max_length=250, blank=True, null=True)
    grade_required = models.CharField(max_length=250, blank=True, null=True)
    pre_requisites_met = models.BooleanField(null=True, blank=True)
    approved_status = models.BooleanField(blank=False, null=True)
    comparison_result = models.JSONField(null=True, blank=True)
    running_comparison = models.BooleanField(default=False)

    class Meta:
        ordering = ['course_application_id']