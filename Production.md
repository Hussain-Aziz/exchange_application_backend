# Steps to deploy the project on a production server

This assumes an ubuntu server is being used.

## Prerequisites

1. Download tesseract for the comparison of pdfs by run `sudo apt-get install -y tesseract-ocr && sudo apt-get install -y poppler-utils`
2. Download postgres thing `sudo apt-get install libpq-dev`
3. Download nginx `sudo apt-get install nginx`

## Initial setup

```bash
# clone the repository
mkdir exchange_application_backend
cd exchange_application_backend
git init
git remote add origin https://github.com/Hussain-Aziz/exchange_application_backend.git
git fetch
git pull origin master

# setup virtual environment
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.11
sudo apt-get install python3.11-venv
python3.11 -m venv exchange_application_venv --clear
source ./exchange_application_venv/bin/activate

# install dependencies
pip install -r config/requirements/base.txt
```

### Environment variables

The app requires the following environment variables to be set (in an .env file in the root dir)

```bash
OPENAI_API_KEY
ANTHROPIC_API_KEY
SECRET_KEY
DB_NAME
DB_USERNAME
DB_PASSWORD
DB_HOST
DB_PORT
```

where secret key is the django secret key which can be generated in django shell by running

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### NGINX

create the directory /etc/nginx/sites-enabled and add this to /etc/nginx/sites-enabled/exchange

``` nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

then edit the nginx.conf file and remove the line `include /etc/nginx/conf.d/*.conf;` and add `include /etc/nginx/sites-enabled/*;`
then restart nginx `sudo systemctl restart nginx`

### SSL Certificates

Using ZeroSSL generate a new certificate from <https://app.zerossl.com/certificate/new>
then to verify create the directory `mkdir /home/ubuntu/static` and add to it the txt file for verification
then add the following to the django nginx file

```nginx
    location /.well-known/pki-validation/ {
        alias /home/ubuntu/static/;
        try_files $uri =404;
    }
```

after verification download the ceritificate zip and move it to /home/ubuntu/certificate/

Then actually set it up reference: <https://help.zerossl.com/hc/en-us/articles/360058295894-Installing-SSL-Certificate-on-NGINX>

- cd into `cd /home/ubuntu/certificate/` and run `unzip certificate.zip`
- then copy the contents of ca_bundle.crt into certificate.crt
- add the following to django nginx file

```nginx
    listen               443 ssl;    
    ssl                  on;
    ssl_certificate      /home/ubuntu/certificate/certificate.crt;
    ssl_certificate_key  /home/ubuntu/certificate/private.key;
```

then restart nginx `sudo systemctl restart nginx`

After this works, change the nginx to this to force redirection to https

```nginx
server {
    listen 80;
    server_name _;

    location / {
        return 301 https://$host$request_uri;
    }

    location /.well-known/pki-validation/ {
        alias /home/ubuntu/static/;
        try_files $uri =404;
    }
}

server {
    listen 443 ssl;
    server_name _;

    ssl_certificate      /home/ubuntu/certificate/certificate.crt;
    ssl_certificate_key  /home/ubuntu/certificate/private.key;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /.well-known/pki-validation/ {
        alias /home/ubuntu/static/;
        try_files $uri =404;
    }
}
```

## Running the application

Create or go to previous screen

- Create: `screen -S django`
- Resume: `screen -r django`

Run the following

``` bash
source ./exchange_application_venv/bin/activate
python manage.py runserver 0.0.0.0:8000 --settings=exchange_application.prod
```
