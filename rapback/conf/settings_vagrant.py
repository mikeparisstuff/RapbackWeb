
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

STREAM_API_KEY = 'y58efseqbg9z'
STREAM_API_SECRET = 'yfpjbeswsjxy2tmehgw4rnt5ng952w86ur856yzfzyd6fvwg6hrt8wyrnyanwd29'

# print("STREAM_API_KEY: {}, STREAM_API_SECRET:{}".format(STREAM_API_KEY, STREAM_API_SECRET))

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