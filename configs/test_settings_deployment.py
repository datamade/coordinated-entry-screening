SECRET_KEY = 'extremely secret test key'

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travis',
        'USER': 'travis',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
} 

ACCOUNT_SID = ''
AUTH_TOKEN = ''
TWILIO_NUMBER = ''

ALLOWED_HOSTS = ['127.0.0.1', '.datamade.us']