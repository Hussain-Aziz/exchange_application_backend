# Exchange Application Backend

## Building steps

### Prerequisites

1. Download python 3.11.7 from <https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe>
2. Download tesseract for the comparison of pdfs
    - windows: download from [here](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-3.05.00dev-205-ge205c59.exe) and set it up.
    - linux: run `sudo apt-get install -y tesseract-ocr && sudo apt-get install -y poppler-utils`

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

### Testing

```bash
python manage.py test
```

for coverage

```bash
coverage run --source='.' manage.py test
coverage report
```
