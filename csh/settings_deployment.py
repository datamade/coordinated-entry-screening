SECRET_KEY = 'Il volo così fido'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'csh',
        'USER': '',
        'PASSWORD': '',
        'PORT': 5432,
    }
}