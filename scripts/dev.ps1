# define the commands to run in the backend
$backend1 = '. .\exchange_application_venv\Scripts\activate.ps1;'
$backend2 = 'python manage.py runserver'
$backend = $backend1 + $backend2

# Start the Django server in a new PowerShell window
Start-Process powershell -ArgumentList '-NoExit', '-Command', $backend