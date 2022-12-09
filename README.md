# Installation

1. Move the NER model (`model-best`) folder inside `receipts_processing/ner-models/`

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

      Note: _If you have a Mac_ system you may not be able to install `paddleocr`. The reason for that is because it uses `PyMuPDF==1.19.0`, which can't be installed in Apple Silicon chips. To solve that, you need to clone the [`paddleocr`](https://github.com/PaddlePaddle/PaddleOCR) repo and override the version of PyMuPDF. To do that, follow these steps:

      1. Install PyMuPF dependencies using [brew](https://brew.sh/)

         ```bash
         brew install mupdf swig freetype
         ```

      2. Install PyMuPDF from source

         ```bash
         pip install https://github.com/pymupdf/PyMuPDF/archive/master.tar.gz
         ```

      3. Clone the [`paddleocr`](https://github.com/PaddlePaddle/PaddleOCR) repo
         ```bash
         git clone https://github.com/PaddlePaddle/PaddleOCR
         ```
      4. Open the repo with your editor, for example `code PaddleOCR`, then find every occurrence of `PyMuPDF==1.19.0` and replace it with `PyMuPDF==1.21.0`.

      5. Inside the `PaddleOCR` folder run

         ```bash
         pip install -r requirements.txt
         ```

         That will install all dependencies required for paddleocr.

      6. Install `paddlepaddle`

         ```bash
         pip install paddlepaddle
         ```

      7. Outside of `PaddleOCR` folder, install `paddleocr` from your local directory by running

         ```bash
         pip install ./PaddleOCR
         ```

         7. Execute general installation steps above.
3. Migrate the database:
   ```bash
   python manage.py migrate
   ```

# Usage

Open your terminal and `cd cpsc-4820-final-project`.

Then run:

```bash
python manage.py runserver
```

That should get Django started and you should be able to see the app running at http://localhost:8000

## Admin panel

We are using Django's built-in admin panel.

To create the admin user you need to run:

```bash
python manage.py createsuperuser
```

It will ask you to set an username, password and email. After you create the super user, you can log in at http://localhost:8000/admin

## URLs

|Path|Method|Description|
|----|------|-----------|
|/|GET|Returns the homepage|
|receipts/new|GET|Returns the form to upload a new receipt|
|receipts/new|POST|Processes the new receipt form data and file
|receipts/int:id|GET|Shows receipt details
|receipts/int:id/file/view|GET|Shows a visualization of the receipt in the receipt details page
|receipts/int:id/file/download|GET|Downloads the receipt|
|receipts/int:id/delete|GET|Deletes the receipt|
|admin|GET|Access the admin panel|
|login|GET|Returns the login page|

## Access to Google APIs

We have created a Google account so we can have access to Google APIs. To access the Google account for this project, use the following credentials:

**E-mail:** receiptsprocessing.cpsc4820@gmail.com

**Password:** cpsc4820

To see **enabled APIs** for this account, log in and visit: https://console.cloud.google.com/apis/dashboard?authuser=1&project=aerial-reality-370603

In order to access those enabled APIS, we need **credentials**: https://console.cloud.google.com/apis/credentials?authuser=1&project=aerial-reality-370603

Credentials are located at `receipts_processing/google/credentials.json`

Since this is a non verified by Google app, only test users are allowed. `receiptsprocessing.cpsc4820@gmail.com` has also been added as a test user.

# Settings

In addition to Django's default settings, we have set the following variables in `settings.py`.

- `ALLOWED_HOSTS` to   `['localhost', '127.0.0.1']`. This is needed when `DEBUG = False`. You may need to set `DEBUG = False` if you want Django to hide errors and return 404 or 500 error pages.

- `INSTALLED_APPS`, in addition to Django's default installed apps (everything `django.contrib.*`), we installed: 
   -  `'receipts_processing.apps.ReceiptsProcessingConfig'`, our app
   - [`'jazzmin'`](https://django-jazzmin.readthedocs.io/), to customize the appearance of the admin panel. This one should always be located before `'django.contrib.admin'` , so it can modify the admin before it is started/created.
   - [`'django.contrib.humanize'`](https://docs.djangoproject.com/en/4.1/ref/contrib/humanize/), a set of template filters provided by Django. We are using the `naturaltime` filter to show the time elapsed since the creation of the receipts. 
   - [`'django.contrib.staticfiles'`](https://docs.djangoproject.com/en/4.1/howto/static-files/), provided by Django to help manage static files.

- `ROOT_URLCONF` to specify the module where we are registering urls for all the apps.

- `DATABASES` to specify the database to use with the app.

   It's recommended you use `sqlite3` for development as it is easier to start with.
   
   To use `sqlite3` set `DATABASES` to:
   ```python
      DATABASES = {
         'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            "NAME": BASE_DIR / "db.sqlite3",
         }
      }
   ```

   If you want to use PostgreSQL, update `DATABASES` to:
   ```python
      DATABASES = {
         'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mydatabase',
            'USER': 'mydatabaseuser',
            'PASSWORD': 'mypassword',
            'HOST': '127.0.0.1',
            'PORT': '5432',
         }
      }
   ```

- `STATIC_URL` to indicate to Django the URL to use when referring to static files.

- `LOGIN_REDIRECT_URL` to indicate where to redirect the user after login.

- `LOGOUT_REDIRECT_URL` to indicate where to redirect the user after logout.

- `LOGIN_URL` to indicate the url for the login page.

- `GMAIL_SYNC_ENABLED` set to False to disable the processing of receipts received via email.

# Drive file sync

The `receipts_processing` app is using Google's API client for Python to back up files to Google Drive.

Receipts are uploaded to folders associated to the user. For example, if `receipt.user.id` is `1`, the receipt file is uploaded to the `1` folder.

Before uploading the receipt, we first check if the user folder has been created before. If so, we use that folder as the parent for the new uploaded file. If there's no folder matching the user id, we create a new folder and then upload the file to it.


The code for receipts back up is located in `receipts_processing/drive.py`.

# Receipts Received via Gmail

The code for this feature can be found at `receipts_processing/email_receipts.py`

We are using Gmail API v1: https://developers.google.com/gmail/api/reference/rest

To make our app able to fetch receipts from Gmail at the same time as the Django app is running, we are using a scheduling library called [APScheduler](https://apscheduler.readthedocs.io/en/3.x/). With the help of the scheduler we can call the function that fetch emails every 5 mins.

Everytime `python manage.py runserver` is run, Django loads the app twice to be able to reload the app whenever the code changes. Therefore the method `ready` is called every time the app gets initilized. Since we are scheduling the task to read attachments from Gmail inside the `ready` function, it gets scheduled twice, therefore the receipts received via email are processed twice. To bypass this behavior, run the app using:

```bash
python manage.py runserver --noreload
```
That will tell Django to run the app once. Keep in mind that the app will not be reloaded automatically if you change the code.

If you want to disable the processing of receipts received via email, set `GMAIL_SYNC_ENABLED = False` in `settings.py`.

Note: Only receipts sent by users registered in the app will be processed.

# NER Model

The code developed for the *CPSC-4830 Data Mining for Data Analytics* final project is included in `receipts_processing/filereader.py`, where the text from each receipt is extracted according to its type, and `receipts_processing/receipts.py`, where the Named Entity Recognition model developed with `Spacy` is applied to the text extracted and the resulting entities are returned. The model is saved at `receipts_processing/ner-models/model-best`.