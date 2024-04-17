from rest_framework.test import APITestCase, APIClient
from users.models import Faculty, User, Student, University
from users.models import CourseApplication
from django.urls import reverse
from knox.auth import AuthToken
import json

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
