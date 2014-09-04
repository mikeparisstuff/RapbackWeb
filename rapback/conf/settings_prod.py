import os

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'RapbackProd',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': 'ec2-54-165-7-42.compute-1.amazonaws.com',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': os.environ['RDS_PORT'],                      # Set to empty string for default.
    }
}
AWS_STORAGE_BUCKET_NAME = 'rapbackprod'

# Celery
BROKER_URL = "sqs://sqs.us-east-1.amazonaws.com/487142144782/rapback-celery-broker//"

# Default to AWS creds. Won't be able to access without permissions
FEEDLY_REDIS_CONFIG = {
    'default': {
        'host': 'ec2-54-210-10-162.compute-1.amazonaws.com',
        'port': 6379,
        'db': 0,
        'password': None
    },
}