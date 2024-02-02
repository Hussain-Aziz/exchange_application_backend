Write-Host "Creating virtual environment..."
# check if python version is 3.11.7
$pythonVersion = python --version
if ($pythonVersion -ne "Python 3.11.7") {
    Write-Host "Python version is not 3.11.7. Please install Python 3.11.7 and try again."
    exit 1
}
python -m venv exchange_application_venv --clear
. .\exchange_application_venv\Scripts\activate

Write-Host "Installing python requirements..."
pip install -r config\requirements\local.txt --require-virtualenv --quiet

Write-Host "Setting up database..."
python manage.py makemigrations --no-input --verbosity 0
python manage.py migrate --no-input --verbosity 0

Write-Host "Finishing backend setup..."
deactivate