# Exchange Application Backend

## Building steps

### Prerequisites

1. Download python 3.11.7 from <https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe>

### Initial setup

1. Open a powershell terminal and navigate to the directory where you want the project
2. Run the following commands

```bash
# clone the repository
git clone git@github.com:Hussain-Aziz/exchange_application_backend.git
cd exchange_application_backend

# setup virtual environment
python -m venv exchange_application_venv --clear
. .\exchange_application_venv\Scripts\activate

# install dependencies
pip install -r config\requirements\local.txt --require-virtualenv --quiet

# run database migrations
python manage.py makemigrations --no-input --verbosity 0
python manage.py migrate --no-input --verbosity 0
python manage.py loaddata exchange_application/seeds/faculty.json
```

### Running the application

1. Open vscode and open the project folder
2. Open a powershell terminal and run the following commands

```bash
. .\exchange_application_venv\Scripts\activate.ps1
python manage.py runserver
```

Create new data

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
