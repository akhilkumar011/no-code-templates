import pymongo

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8081',  # Correct: Without the trailing slash and path
    # Other allowed origins...
]
STAGE = 'TEST'
DATABASES = {
    # 'default': {
    #     'ENGINE': 'djongo',
    #     'ENFORCE_SCHEMA': True,
    #     'NAME': 'Hb_ERP_Utility',  # Name of your MongoDB database
    #     'HOST': 'localhost',  # MongoDB server host (default is localhost)
    #     'PORT': 27017,  # MongoDB server port (default is 27017)
    # }
}

# Master Database for Project
DB_HOST = "localhost"
DB_PORT = 27017
DB_NAME = "Hb_ERP_Utility"
DB_USER = "hbuser"
DB_PASS = "Admin@1234"
DB_URI = 'mongodb://localhost:27017/'

# For Data Utility Service
ACT_DB_HOST = "localhost"
ACT_DB_PORT = 27017
ACT_DB_NAME = "hb_accounting_reporting"
ACT_DB_USER = "hbuser"
ACT_DB_PASS = "Admin@1234"
ACT_DB_URI = 'mongodb://localhost:27017/'
