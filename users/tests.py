from rest_framework.test import APITestCase, APIClient
from users.models import Faculty, User, Student, University
from users.models import CourseApplication
from django.urls import reverse
from knox.auth import AuthToken
from threading import Thread
from users.serializers import StudentApplicationSerializer
from exchange_application.views import UserSerializer
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
        response = self.client.get(reverse('comparison'), {'course_1': 'https://exchange-application-frontend.vercel.app/CMP305.pdf', 'course_2': 'https://exchange-application-frontend.vercel.app/ECE36800.pdf'})
        self.assertEqual(response.status_code, 200)
        
    def test_compare_syllabi_no_params(self):
        self.client.force_authenticate(user=self.user, token=self.token) # type: ignore
        response = self.client.get(reverse('comparison'))
        self.assertEqual(response.status_code, 400)

class TestSeralizer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.student = Student.objects.create(user=self.user, aus_id='b00012345')
    
    def test_seralizer(self):
        StudentApplicationSerializer(self.student)

        
class TestApplicationComparison(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='teststudent', password='testpass')
        self.university = University.objects.create(university_name='test university')
        self.student = Student.objects.create(user=self.user, aus_id='b00012345', university= self.university)
        self.course_application = CourseApplication.objects.create(department=13, course_application_id=999, student=self.student, university=self.university, aus_syllabus='https://exchange-application-frontend.vercel.app/CMP305.pdf', syllabus='https://exchange-application-frontend.vercel.app/ECE36800.pdf')
        AuthToken.objects.create(user=self.user)
        self.token = AuthToken.objects.all()[0].token_key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_comparison(self):
        self.client.force_authenticate(user=self.user, token=self.token) # type: ignore
        response = self.client.get(reverse('compare_application'), {'id': 999})
        self.assertEqual(response.status_code, 200)

    def test_comparison_no_params(self):
        self.client.force_authenticate(user=self.user, token=self.token) # type: ignore
        response = self.client.get(reverse('compare_application'))
        self.assertEqual(response.status_code, 400)

    def test_comparison_bad_params(self):
        self.client.force_authenticate(user=self.user, token=self.token) # type: ignore
        response = self.client.get(reverse('compare_application'), {'id': 123})
        self.assertEqual(response.status_code, 400)

    def test_muli_threaded_comparison(self):
        thread1 = Thread(target=self.test_comparison)
        thread2 = Thread(target=self.test_comparison)
        
        thread1.start()
        time.sleep(5)
        thread2.start()

        for thread in [thread1, thread2]:
            thread.join()

