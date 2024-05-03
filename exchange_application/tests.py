from rest_framework.test import APITestCase, APIClient
from users.models import User, Student, Faculty
from exchange_application.views import UserSerializer
from django.test import TestCase

from django.urls import reverse
from django.contrib.auth.models import User

from .settings import *

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
        self.faculty = Faculty.objects.create(user=self.user, department=13, faculty_type=0, college=3)
        request = self.client.post(reverse('knox_login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(request.status_code, 200)

class TestSeralizer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.student = Student.objects.create(user=self.user, aus_id='b00012345')
    
    def test_seralizer(self):
        UserSerializer(self.user)

class SettingsTest(TestCase):
    def test_vars(self):
        print(BASE_DIR)
        print(SECRET_KEY)
        print(DEBUG)
        print(ALLOWED_HOSTS)
        print(INSTALLED_APPS)
        print(REST_FRAMEWORK)
        print(REST_KNOX)
        print(MIDDLEWARE)
        print(ROOT_URLCONF)
        print(TEMPLATES)
        print(WSGI_APPLICATION)
        print(DATABASES)
        print(AUTH_PASSWORD_VALIDATORS)
        print(LANGUAGE_CODE)
        print(TIME_ZONE)
        print(USE_I18N)
        print(USE_TZ)
        print(STATIC_URL)
        print(DEFAULT_AUTO_FIELD)
        print(AWS_ACCESS_KEY_ID)
        print(AWS_SECRET_ACCESS_KEY)
        print(AWS_STORAGE_BUCKET_NAME)
        print(AWS_S3_FILE_OVERWRITE)
        print(AWS_DEFAULT_ACL)
        print(AWS_S3_REGION_NAME)
        print(AWS_S3_SIGNATURE_VERSION)
        print(AWS_S3_ADDRESSING_STYLE)
        print(DEFAULT_FILE_STORAGE)