# Exchange Application Backend

## Building steps

1. Download python 3.11.7 from [here](https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe)
2. Download and setup tesseract for the comparison of pdfs from [here](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-3.05.00dev-205-ge205c59.exe)

### Initial setup

The commands below are for powershell. If you are running in a linux shell see [production setup](./Production.md)

```bash
# clone the repository
git clone https://github.com/Hussain-Aziz/exchange_application_backend
cd exchange_application_backend

# setup virtual environment
python -m venv exchange_application_venv --clear
. .\exchange_application_venv\Scripts\activate.ps1

# install dependencies
pip install -r config\requirements\base.txt --require-virtualenv --quiet

# run database migrations
python manage.py makemigrations --no-input --verbosity 0
python manage.py migrate --no-input --verbosity 0
```

### Environment variables

The app requires the following environment variables to be set (in an .env file in the root dir)

```bash
OPENAI_API_KEY
ANTHROPIC_API_KEY
SECRET_KEY
```

where secret key is the django secret key which can be generated in django shell by running

```python
from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())
```

Note: Django shell can be accessed by running `python manage.py shell`

### Running the application

1. Open vscode and open the project folder
2. Open a powershell terminal and run the following commands

```bash
. .\exchange_application_venv\Scripts\activate.ps1
python manage.py runserver
```

### Testing

```bash
python manage.py test
```

for coverage

```bash
coverage run --source='.' manage.py test
coverage report
```
