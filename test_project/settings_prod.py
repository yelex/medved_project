DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django-base',
        'USER' : 'hello_django',
        'PASSWORD' : 'Fokina12',
        'HOST' : 'localhost',
        'PORT' : '',
    }
}