DEBUG = False
ALLOWED_HOSTS = ['134.122.82.169', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shop-base',
        'USER' : 'hello_django',
        'PASSWORD' : 'Fokina12',
        'HOST' : 'localhost',
        'PORT' : '',
    }
}
