# Creating base data in database

run `python manage.py shell` and paste the following code inside

```python

from django.contrib.auth.models import User
from users.models import Faculty, Student, Admin

u = User(username="b01@aus.edu")
u.set_password("test")
u.save()
Student.objects.create(user=u)

u = User(username="b02@aus.edu")
u.set_password("test")
u.save()
Student.objects.create(user=u)

u = User(username="b03@aus.edu")
u.set_password("test")
u.save()
Student.objects.create(user=u)

u = User(username="b04@aus.edu")
u.set_password("test")
u.save()
Student.objects.create(user=u)

u = User(username="aa@aus.edu")
u.set_password("test")
u.save()
Faculty.objects.create(user=u, department=13, faculty_type=0, college=3)

u = User(username="hod@aus.edu")
u.set_password("test")
u.save()
Faculty.objects.create(user=u, department=13, faculty_type=2, college=3)

u = User(username="tf01@aus.edu")
u.set_password("test")
u.save()
Faculty.objects.create(user=u, department=13, faculty_type=1, college=3)

u = User(username="tf02@aus.edu")
u.set_password("test")
u.save()
Faculty.objects.create(user=u, department=13, faculty_type=1, college=3)

u = User(username="advisor@aus.edu")
u.set_password("test")
u.save()
Faculty.objects.create(user=u, department=13, faculty_type=3, college=3)

u = User(username="adean@aus.edu")
u.set_password("test")
u.save()
Faculty.objects.create(user=u, department=13, faculty_type=4, college=3)

u = User(username="admin@aus.edu")
u.set_password("test")
u.save()
Admin.objects.create(user=u)

```

Then run the following commands

```bash
python manage.py makesuperuser
python manage.py makemigrations
python manage.py migrate
```
