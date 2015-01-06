import os

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'RapbackProd',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': 'rapbackprodrds.cwbcnf9punqe.us-east-1.rds.amazonaws.com',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': os.environ['RDS_PORT'],                      # Set to empty string for default.
    }
}
AWS_STORAGE_BUCKET_NAME = 'rapback-prod-s3'

STREAM_API_KEY = 'tr9pcvpxke9t'
STREAM_API_SECRET = 'n47xmf6mawd8dusr69bxwn9xhvhjw6wsekdpk2ntfz6wr9xhpu5yf7hmfrkaepjm'

# Celery
BROKER_URL = "sqs://sqs.us-east-1.amazonaws.com/881959240084/RapbackProdQueue//"

# Default to AWS creds. Won't be able to access without permissions
FEEDLY_REDIS_CONFIG = {
    'default': {
        # 'host': 'ec2-54-210-10-162.compute-1.amazonaws.com',
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': None
    },
}