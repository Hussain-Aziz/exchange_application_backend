from rest_framework.test import APITestCase, APIClient
from users.models import Faculty, IXODetails, User, Student, University
from users.models import CourseApplication
from django.urls import reverse
from knox.auth import AuthToken
import json

class TestStartApplicationAPI(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpass')
        self.student = Student.objects.create(user=self.user)
        self.university = University.objects.create(university_name='test university')
        AuthToken.objects.create(user=self.user)
        self.token = AuthToken.objects.all()[0].token_key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_start_application(self):
        self.client.force_authenticate(user=self.user, token=self.token) # type: ignore
        data = {
            'university': 'test university',
            'id': 'b00012345',
            'name': 'test student',
            'mobileNumber': '1234567890',
            'expectedGraduation': '2023',
            'presentCollege': 'CEN',
            'department': 13,
            'presentMajor': 'test major',
            'currentStanding': 'test standing',
            'hostContactName': 'test contact',
            'hostContactEmail': 'test@test.com'
        }
        response = self.client.post(reverse('start_application'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_application(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        response = self.client.delete(reverse('start_application'))
        self.assertEqual(response.status_code, 204)


class TestApplicationInfoAPI(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpass')
        self.university = University.objects.create(university_name='test university')
        self.student = Student.objects.create(user=self.user, aus_id='b00012345', university=self.university)
        AuthToken.objects.create(user=self.user)
        self.token = AuthToken.objects.all()[0].token_key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_application_info(self):
        self.client.force_authenticate(user=self.user, token=self.token) # type: ignore
        response = self.client.get(reverse('application_info'))
        self.assertEqual(response.status_code, 200)


class TestAddCourseAPI(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpass')
        self.university = University.objects.create(university_name='test university')
        self.student = Student.objects.create(user=self.user, aus_id='b00012345', university=self.university)
        self.course = CourseApplication.objects.create(student=self.student, university=self.university)
        AuthToken.objects.create(user=self.user)
        self.token = AuthToken.objects.all()[0].token_key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_add_course(self):
        self.client.force_authenticate(user=self.user, token=self.token) # type: ignore
        data = {
            'hostCourseCode': 'test code',
            'hostCouseTitle': 'test title',
            'courseCredits': '3',
            'ausCourse': 'STA 301',
            'hostUniversitySyllabus': 'test syllabus',
            'ausausSyllabus': 'test syllabus'
        }
        response = self.client.post(reverse('courses'), json.dumps(data), content_type='application/json')

    def test_get_courses(self):
        self.client.force_authenticate(user=self.user, token=self.token) # type: ignore
        response = self.client.get(reverse('courses'))
class SubmitApplication(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpass')
        self.university = University.objects.create(university_name='test university')
        self.student = Student.objects.create(user=self.user, aus_id='b00012345', university=self.university, ixo_details=IXODetails.objects.create())
        AuthToken.objects.create(user=self.user)
        self.token = AuthToken.objects.all()[0].token_key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_submit(self):
        self.client.force_authenticate(user=self.user, token=self.token) # type: ignore
        response = self.client.post(reverse('submit_application'), json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
