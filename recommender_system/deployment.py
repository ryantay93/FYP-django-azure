import os
from .settings import *
# from .settings import BASE_DIR

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]
DEBUG = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
#    'whitenoise.middleware.whiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

'''
# Might need to pip install whitenoise for static files
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_ROOT = BASE_DIR / 'static'
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Might need to pip install python-dotenv for this part
connection_string = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
parameters = {pair.split('='):pair.split('=')[1] for pair in connection_string.split(' ')}

# Might need to pip install psycopg2 to use a different database
DATABASES = {
    
    'default' : {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parameters['dbname'],
        'HOST': parameters['host'],
        'USER': parameters['user'],
        'PASSWORD': parameters['password'],
        
    }
    
}
'''