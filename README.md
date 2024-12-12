# Quiz Game API

This is a Django-based API for a Quiz Game application. It provides endpoints for user authentication, quiz management, and more.

## Project Structure

- **apps/users**: Contains the user management module, including models, views, and migrations.
- **config**: Contains the project settings, URLs, and WSGI/ASGI configurations.

## Setup Instructions

### Prerequisites

- Python 3.10+
- PostgreSQL
- Virtualenv

### Local Development Setup

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd QUIIZ-GAME
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements/dev.txt
   ```

4. **Configure environment variables**:

   copy `.env.example` in `config/settings` folder to `.env` and set the necessary environment variables. Refer to `config/settings/common.py` for required variables.

5. **Setup the database**:

   Ensure PostgreSQL is running and create a database for the project. Update the `DATABASE_URL` in your `.env` file accordingly.

6. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

7. **Run the development server**:

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

### Creating New Migrations

To create new migrations after modifying models, run:

```bash
python manage.py makemigrations
```

Then apply the migrations with:

```bash
python manage.py migrate
```

### Adding New Modules

1. **Create a new app**:

   ```bash
   python manage.py startapp <app_name>
   ```

## Generating JWT Keys

To generate the JWT private and public keys, follow these steps:

1. **Generate the private key**:
   
   ```bash
   openssl genpkey -algorithm RSA -out jwt_api_key
   ```

2. **Extract the public key from the private key**:

   ```bash
   openssl rsa -pubout -in jwt_api_key -out jwt_api_key.pub
   ```

Make sure to keep the `jwt_api_key` file secure and do not expose it publicly.

## Django Admin
- URL: http://localhost/admin

## Swagger Document
- URL: http://localhost/docs

## API Authentication
- JWT Authentication is supported


## Handwriting Recognition with Open-Source Tools

1. **Create/or copy a recognitions app**:
   ```bash
   Copy an recognitions app from one app to another in the new project.
   or
   django-admin startapp recognitions
   ```

2. **Copy training-data folder/ or create new folder with name is training-data**:
   ```bash
   In here including:
   [data, data2] using to train internal TensorFlow. Downloaded from the experimental training model website:
         https://drive.google.com/file/d/1k6H9kQWfzLJB-ajuT6j4U0H0vyx7n_uL/view?usp=drive_link
   [emnist_external_model.h5] using the external TensorFlow EMNIST library to train and generate this file when running the API:
         /recognitionsapi/train-tensorflow-emnist-external/
   [handwriting_internal_model.h5] using the internal TensorFlow library to train and generate this file when running the API:
         /recognitionsapi/train-tensorflow-internal/
   [loss_graph_emnist_external.png, loss_graph_internal.png] Plot the loss graph after training is complete.
   ```

3. **In config/settings/common.py to add 'apps.recognitions.apps.RecognitionsConfig' inside LOCAL_APPS**:
   ```bash
   LOCAL_APPS = (
      ...
      'apps.recognitions.apps.RecognitionsConfig',
   )
   CORS_ALLOWED_ORIGINS = [
      ...
      "http://localhost:8000",  # Allow from localhost 
      "http://127.0.0.1:8000",  # Or from the localhost IP address
   ]
   ```

4. **In config/api.py to add path("recognitions/", include("apps.recognitions.api.recognition_url")),**:
   ```bash
   urlpatterns = [
      ...
      path("recognitions/", include("apps.recognitions.api.recognition_url")),
   ]
   ```

5. **In requirements/dev.txt to add Handwriting Recognition with Open-Source Tools**:
   ```bash
   ```

6. **And then running tep 2, 3, 6. **Run migrations** & 7. **Run the development server** as above**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `.\venv\Scripts\activate` & python.exe -m pip install --upgrade pip
   pip install -r requirements/dev.txt
   ------------------------
   pip install paddlepaddle  # Note 1: PaddlePaddle needs to be reinstalled, because the paddlepaddle depends on protobuf <=3.20.2 while the tensorflow depends on protobuf >=3.20.3 
   ------------------------
   python manage.py makemigrations
   python manage.py migrate
   ------------------------
   python manage.py runserver 0.0.0.0:8000  # On localhost: python manage.py runserver localhost:8000
   
   ## Django Admin
   - URL: http://localhost/admin
   
   ## Swagger Document
   - URL: http://localhost/docs
   ```

7. **How to modify training data? Just copy the new images containing the letter characters into the correct folder and run the training API again (use Internal libraries).**:
   ```bash
   ## Train data from API:
      API: Internal libraries
         /recognitions/api/train-tensorflow-internal/
      API: External emnist libraries
         /recognitions/api/train-tensorflow-emnist-external/
   ## Handwriting Recognition from API:
      API: Internal libraries
         /recognitions/api/tensorflow-internal/
      API: External emnist libraries
         /recognitions/api/tensorflow-emnist-external/
   ```

8. **Some APIs operate in sequence from the training API to the handwriting recognition API.**:
   ```bash
   ## Internal libraries
      /recognitions/api/train-tensorflow-internal/
      /recognitions/api/tensorflow-internal/
   ## External emnist libraries
      /recognitions/api/train-tensorflow-emnist-external/
      /recognitions/api/tensorflow-emnist-external/
   ```
