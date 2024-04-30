from rest_framework.test import APITestCase, APIClient
from users.models import Faculty, IXODetails, User, Student, University
from users.models import CourseApplication
from django.urls import reverse
from knox.auth import AuthToken
from student.seralizers import FacultySerializer, UserSerializer, StudentApplicationSerializer, IXODetailsSerializer, UniversitySerializer, CourseApplicationSerializer
import time
from django.test import TestCase

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

class TestComparisonAPI(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        AuthToken.objects.create(user=self.user)
        self.token = AuthToken.objects.all()[0].token_key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_compare_syllabi(self):
        self.client.force_authenticate(user=self.user, token=self.token) # type: ignore
        response = self.client.get(reverse('comparison'), {'course_1': 'https://ausxchange.com/CMP305.pdf', 'course_2': 'https://ausxchange.com/ECE36800.pdf'})
        self.assertEqual(response.status_code, 200)
        
    def test_compare_syllabi_no_params(self):
        self.client.force_authenticate(user=self.user, token=self.token) # type: ignore
        response = self.client.get(reverse('comparison'))

class TestSeralizer(TestCase):
    def setUp(self):
        self.university = University.objects.create(university_name='test university')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.student = Student.objects.create(user=self.user, aus_id='b00012345')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass')
        self.faculty = Faculty.objects.create(user=self.user2, department=13, faculty_type=0)
        self.course = CourseApplication.objects.create(department=13, course_application_id=999, student=self.student, university=self.university)
        self.ixo_details = IXODetails.objects.create()
    
    def test_seralizer(self):
        StudentApplicationSerializer(self.student)
        FacultySerializer(self.faculty)
        IXODetailsSerializer(self.student.ixo_details)
        UniversitySerializer(self.student.university)
        CourseApplicationSerializer(self.course)
        UserSerializer(self.user)

        
class TestApplicationComparison(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='teststudent', password='testpass')
        self.university = University.objects.create(university_name='test university')
        self.student = Student.objects.create(user=self.user, aus_id='b00012345', university= self.university)
        self.course_application = CourseApplication.objects.create(department=13, course_application_id=999, student=self.student, university=self.university, aus_syllabus='https://ausxchange.com/CMP305.pdf', syllabus='https://ausxchange.com/ECE36800.pdf')
        AuthToken.objects.create(user=self.user)
        self.token = AuthToken.objects.all()[0].token_key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_comparison(self):
        self.client.force_authenticate(user=self.user, token=self.token) # type: ignore
        response = self.client.get(reverse('compare_application'), {'id': 999})

    def test_comparison_no_params(self):
        self.client.force_authenticate(user=self.user, token=self.token) # type: ignore
        response = self.client.get(reverse('compare_application'))

    def test_comparison_bad_params(self):
        self.client.force_authenticate(user=self.user, token=self.token) # type: ignore
        response = self.client.get(reverse('compare_application'), {'id': 123})
