# Creating base data in database

run `python manage.py shell` and paste the seed function inside

```python
def seed():
    from django.contrib.auth.models import User
    from users.models import Faculty, Student

    u1 = User(username="izualkernan@aus.edu")
    u1.set_password("test")
    u1.save()
    u2 = User(username="dcjuan@aus.edu")
    u2.set_password("test")
    u2.save()
    u3 = User(username="ddghaym@aus.edu")
    u3.set_password("test")
    u3.save()
    u4 = User(username="b00088793@aus.edu")
    u4.set_password("test")
    u4.save()
    Faculty(user=u1, department=12, faculty_type=2).save()
    Faculty(user=u2, department=12, faculty_type=0).save()
    Faculty(user=u3, department=12, faculty_type=1).save()
    Student(user=u4).save()
```

Then call seed() and exit the shell and then do

```bash
python manage.py makesuperuser
python manage.py makemigrations users
python manage.py migrate
```
