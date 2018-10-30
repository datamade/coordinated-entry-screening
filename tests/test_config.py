SECRET_KEY = 'test test test'

INSTALLED_APPS = [
    'ces_client',
    'ces_admin',
    'rapidsms',
    # third party apps.
    'django_tables2',
    'selectable',
    'decisiontree',
    'rtwilio',
    # django contrib apps
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    # rapidsms contrib apps.
    'rapidsms.contrib.handlers',
    'rapidsms.contrib.httptester',
    'rapidsms.contrib.messagelog',
    'rapidsms.contrib.messaging',
    'rapidsms.contrib.registration',
    'rapidsms.contrib.echo',
    'rapidsms.router.db',
    'rapidsms.backends.database',
    'rapidsms.backends.kannel',
    'rapidsms.tests.translation',

    'rapidsms.contrib.default',  # Should be last
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'coordinated-entry-screening',
        'USER': '',
        'PASSWORD': '',
        'PORT': 5432,
    }
} 

ROOT_URLCONF = 'coordinated-entry-screening.urls'