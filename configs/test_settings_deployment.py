SECRET_KEY = 'extremely secret test key'

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'coordinated-entry-screening',
        'USER': '',
        'PASSWORD': '',
        'PORT': 5432,
    }
} 

ACCOUNT_SID = ''
AUTH_TOKEN = ''
TWILIO_NUMBER = ''

ALLOWED_HOSTS = ['127.0.0.1', '.datamade.us']