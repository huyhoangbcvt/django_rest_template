# django_rest
Init Django Rest Framework 

# Create project
django-admin startproject django_rest

# path to project folder
cd django_rest

# Create apps
django-admin startapp user_app

django-admin startapp catalog_app

pip install -r requirements.txt

# Create db_name django_rest_template in PostreSQL & config DATABASES in settings.py file

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

# Run on browser
http://localhost:8083/

# Run user & catalog
http://localhost:8083/user/api/

http://localhost:8083/catalog/api/

# Run admin site
http://localhost:8083/admin/

# APIs
# Groups
http://localhost:8083/user/api/groups/

# Register
http://localhost:8083/user/api/sign-up/

# List users
http://localhost:8083/user/api/users/

# Register: djoser endpoints
http://localhost:8083/user/api/auth/users/

# Get token user
http://localhost:8083/user/api/get-token/

# Login to get token user
http://localhost:8083/user/api/login/

# Get refresh token & access token: djoser endpoints
http://localhost:8083/user/api/auth/jwt/create/

# Get refresh token & access token
http://localhost:8083/user/api/refresh-token/

# Categories list
http://localhost:8083/catalog/api/category/

# Category add
http://localhost:8083/catalog/api/category/add/?role=Guess&username=it.hoanghh

# Products list
http://localhost:8083/catalog/api/product/

# Product add
http://localhost:8083/catalog/api/product/add/?role=Guess&username=it.hoanghh

# All display on swagger
http://localhost:8083/django/swagger/
