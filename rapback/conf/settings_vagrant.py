
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'rapback_vagrant2',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'TEST_NAME': 'rapchat_test',
            'USER': 'django_login',
            'PASSWORD': 'django_login',
            'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
    }
}

STREAM_API_KEY = '5f6tkb3gpft2'
STREAM_API_SECRET = '9b7ubxw9r5ewtq6nzs9p7fvs324rnjx8hb9hy3ue3z2zvw3ghb64nfg9f4s28z73'

# Celery
BROKER_URL = "sqs://sqs.us-east-1.amazonaws.com/487142144782/vagrant-celery-broker"

# Redis
FEEDLY_REDIS_CONFIG = {
    'default': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': None
    },
}

AWS_STORAGE_BUCKET_NAME = 'rapback-test-s3'