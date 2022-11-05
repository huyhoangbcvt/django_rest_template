# django_rest
Init Django Rest Framework 

## Prerequisites
- Python 3.8 +
- Virtualenv
- Postgres 9.6 +

# Create project (Ignore if clone source code)
django-admin startproject django_rest_template

# path to project folder
cd django_rest_template

# Create apps (Ignore if clone source code)
django-admin startapp user_app

django-admin startapp catalog_app

django-admin startapp upload_app

# install pip
pip install pip

# Create and activate virtualenv
virtualenv venv
.\venv\Scripts\activate

pip install -r requirements.txt

# Create db_name django_rest_template in postgreSQL & config DATABASES in settings.py file
## Installation
### Setup django_rest_template/settings.py

# Create migrations standard
python manage.py makemigrations

# if migrations a app detail, example user_app
python manage.py makemigrations user_app

# Apply into DB
python manage.py migrate
# if migrate a app detail, example user_app
python manage.py migrate user_app

# Create account admin
python manage.py createsuperuser

# if using port default 8000
python manage.py runserver
# if using port other, ex 8083
python manage.py runserver localhost:8083

# Run web on browser for user
http://localhost:8083/

# Run web on browser for admin site 
http://localhost:8083/admin/

# Get refresh token & access token
http://localhost:8083/user/api/refresh-token/

# Implement APISs user, catalog, upload -> domain/app_name/api/
http://localhost:8083/user/api/

http://localhost:8083/catalog/api/

Or 

# APIs: all in api/swagger/  or  api/redoc/
# This All display on swagger
http://localhost:8083/api/swagger/

# Or
http://localhost:8083/api/redoc/

