import logging, os
IS_DEV = os.getenv('IS_DEV')
logging.warning(IS_DEV)
DEBUG = False

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
