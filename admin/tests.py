from rest_framework.test import APITestCase, APIClient
from users.models import Faculty, User, Student, University, Admin
from users.models import CourseApplication
from django.urls import reverse
from knox.auth import AuthToken
import json

class TestFacultyList(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create(username='testadmin', password='testpass')
        self.admin = Admin.objects.create(user=self.admin_user)
        self.faculty = Faculty.objects.create(user=User.objects.create(username='testf', password='testpass'), department=13, college=3, faculty_type=2)
        AuthToken.objects.create(user=self.admin_user)
        self.token = AuthToken.objects.all()[0].token_key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_faculty_list(self):
        self.client.force_authenticate(user=self.admin_user, token=self.token) # type: ignore
        response = self.client.get(reverse('faculty'))
        self.assertEqual(response.status_code, 200)
    
    def test_post_faculty_list(self):
        self.client.force_authenticate(user=self.admin_user, token=self.token) # type: ignore
        data = {'id': self.faculty.id, 'department': 14, 'faculty_type': 3}
        response = self.client.post(reverse('faculty'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Faculty updated successfully')
        updated_faculty = Faculty.objects.get(id=self.faculty.id)
        self.assertEqual(updated_faculty.department, 14)
        self.assertEqual(updated_faculty.faculty_type, 3)
        
        
class TestStudentList(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create(username='testadmin', password='testpass')
        self.admin = Admin.objects.create(user=self.admin_user)
        self.faculty = Faculty.objects.create(user=User.objects.create(username='testf', password='testpass'), department=13, college=3, faculty_type=2)
        AuthToken.objects.create(user=self.admin_user)
        self.token = AuthToken.objects.all()[0].token_key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_student_list(self):
        self.client.force_authenticate(user=self.admin_user, token=self.token) # type: ignore
        response = self.client.get(reverse('student'), {'only_new_students': True})
        response = self.client.get(reverse('student'), {'only_final_approval': True})
        response = self.client.get(reverse('student'), {'only_in_progress': True})
    

class TestInitialApproval(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create(username='testadmin', password='testpass')
        self.admin = Admin.objects.create(user=self.admin_user)
        self.student = Student.objects.create(user=User.objects.create(username='teststudent', password='testpass'))
        AuthToken.objects.create(user=self.admin_user)
        self.token = AuthToken.objects.all()[0].token_key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_initial_approval(self):
        self.client.force_authenticate(user=self.admin_user, token=self.token) # type: ignore
        data = {
            'id': self.student.id,
            'moeApproval': 'true',
            'usdoeApproval': 'true',
            'acreditted': 'true',
            'acredittedComments': 'Test comment',
            'agreement': 'true'
        }
        response = self.client.post(reverse('new_application'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Initial approval saved successfully')
        student = Student.objects.get(id=self.student.id)
        self.assertIsNotNone(student.ixo_details)
        self.assertEqual(student.ixo_details.moe_approval, True)
        self.assertEqual(student.ixo_details.usdoe_approval, True)
        self.assertEqual(student.ixo_details.acreditted, True)
        self.assertEqual(student.ixo_details.acreditted_comments, 'Test comment')
        self.assertEqual(student.ixo_details.agreement, True)
        
        
class TestFinalApproval(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create(username='testadmin', password='testpass')
        self.admin = Admin.objects.create(user=self.admin_user)
        self.student = Student.objects.create(user=User.objects.create(username='teststudent', password='testpass'))
        AuthToken.objects.create(user=self.admin_user)
        self.token = AuthToken.objects.all()[0].token_key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_initial_approval(self):
        self.client.force_authenticate(user=self.admin_user, token=self.token) # type: ignore
        data = {
            'id': self.student.id,
            'studentType': 'Test student type',
            'finalApproval': 'true'
        }
        response = self.client.post(reverse('final_approval'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

class TestCoursesList(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create(username='testadmin', password='testpass')
        self.admin = Admin.objects.create(user=self.admin_user)
        self.student = Student.objects.create(user=User.objects.create(username='teststudent', password='testpass'))
        self.university = University.objects.create(university_name='Test university')
        self.course_application = CourseApplication.objects.create(student=self.student, university=self.university)
        AuthToken.objects.create(user=self.admin_user)
        self.token = AuthToken.objects.all()[0].token_key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_courses_list(self):
        self.client.force_authenticate(user=self.admin_user, token=self.token) # type: ignore
        response = self.client.get(reverse('courses'), {'student_id': self.student.id})
        self.assertEqual(response.status_code, 200)
        
    def test_patch_courses_list(self):
        self.client.force_authenticate(user=self.admin_user, token=self.token) # type: ignore
        data = {'id': self.course_application.course_application_id, 'assignedTo': 'Test assignee'}
        response = self.client.patch(reverse('courses'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

