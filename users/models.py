from django.db import models

# Create your models here.
class Faculty(models.Model):
    faculty_id = models.IntegerField(primary_key=True)
    department = models.CharField(max_length=35)
    faculty_name = models.CharField(max_length=30)

    def __str__(self):
            return self.faculty_name
    

class University(models.Model):
    university_id = models.IntegerField(primary_key=True)
    university_name = models.CharField(max_length=50)

    def __str__(self):
        return self.university_name
    
class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    facultyid = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=20)

    def __str__(self):
        return self.course_name
    
class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    universityid = models.ForeignKey(University, on_delete=models.CASCADE)
    phone_num = models.IntegerField()
    expected_graduation = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class CourseApplication(models.Model):
    course_application_id = models.AutoField(primary_key=True)
    studentid = models.ForeignKey(Student, on_delete=models.CASCADE)
    courseid = models.ForeignKey(Course, on_delete=models.CASCADE)
    universityid = models.ForeignKey(University, on_delete=models.CASCADE)
    semester = models.CharField(max_length=15)
    facultyid = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student} - {self.course}"