from rest_framework.test import APITestCase, APIClient
from users.models import Faculty, User, Student, University
from users.models import CourseApplication
from django.urls import reverse
from knox.auth import AuthToken
import json

class TestViews(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.faculty_user = User.objects.create(username='testfaculty', password='testpass')
        self.faculty = Faculty.objects.create(user=self.faculty_user, department=13)
        self.university = University.objects.create(university_name='test university')
        self.student = User.objects.create(username='teststudent', password='testpass')
        self.student = Student.objects.create(user=self.student, aus_id='b00012345', university= self.university)
        self.course_application = CourseApplication.objects.create(department=self.faculty.department, course_application_id=999, student=self.student, university=self.university)
        AuthToken.objects.create(user=self.faculty_user)
        self.token = AuthToken.objects.all()[0].token_key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_available_syllabus(self):
        self.client.force_authenticate(user=self.faculty_user, token=self.token) # type: ignore
        response = self.client.get(reverse('available_syllabus'))
        self.assertEqual(response.status_code, 200)

    def test_upload_syllabus(self):
        self.client.force_authenticate(user=self.faculty_user, token=self.token) # type: ignore
        response = self.client.post(reverse('upload_syllabus'), json.dumps({'id': '999', 'syllabus': 'https://link.test'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.course_application.refresh_from_db()
        self.assertEqual(self.course_application.aus_syllabus, 'https://link.test')

    def test_approve_course(self):
        self.client.force_authenticate(user=self.faculty_user, token=self.token) # type: ignore
        response = self.client.post(reverse('approve_course'), json.dumps({'id': 999, 'programArea': 'test program', 'gradeRequirement': 'C', 'preReqsMet': True, 'approved': True}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.course_application.refresh_from_db()
        self.assertEqual(self.course_application.program_area, 'test program')
        self.assertEqual(self.course_application.grade_required, 'C')
        self.assertEqual(self.course_application.pre_requisites_met, True)
        self.assertEqual(self.course_application.approved_status, True)

    def test_available_approvals(self):
        self.client.force_authenticate(user=self.faculty_user, token=self.token) # type: ignore
        response = self.client.get(reverse('available_approvals'))
        self.assertEqual(response.status_code, 200)