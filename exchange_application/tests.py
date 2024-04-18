from rest_framework.test import APITestCase, APIClient
from users.models import User, Student, Faculty
from exchange_application.views import UserSerializer
from django.test import TestCase

from django.urls import reverse
from django.contrib.auth.models import User

class LoginViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser')
        self.user.set_password('testpass')
        self.user.save()

    def test_login_student(self):
        self.student = Student.objects.create(user=self.user, aus_id='b00012345')
        request = self.client.post(reverse('knox_login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(request.status_code, 200)

    def test_login_faculty(self):
        self.faculty = Faculty.objects.create(user=self.user, aus_id='b00012345')
        request = self.client.post(reverse('knox_login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(request.status_code, 200)

class TestSeralizer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.student = Student.objects.create(user=self.user, aus_id='b00012345')
    
    def test_seralizer(self):
        UserSerializer(self.user)