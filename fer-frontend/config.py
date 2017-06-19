import os
import logging

PROJECT_ID = 'fer-project-170115'
CLOUD_STORAGE_BUCKET = 'fer-app-engine'
MAX_CONTENT_LENGTH = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
PREDICTION_SERVICE_URL = 'http://130.211.243.194:80'
FIREBASE_URL = 'https://fer-project-170115.firebaseio.com'


# DATA_BACKEND = 'datastore'
# CLOUDSQL_USER = 'root'
# CLOUDSQL_PASSWORD = 'novirus'
# CLOUDSQL_DATABASE = 'fer'
# CLOUDSQL_CONNECTION_NAME = 'fer-project-170115:asia-east1:fer-sql-instance'



# Alternatively, you could use a local MySQL instance for testing.
# LOCAL_SQLALCHEMY_DATABASE_URI = (
#     'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}').format(
#         user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
#         database=CLOUDSQL_DATABASE)

# When running on App Engine a unix socket is used to connect to the cloudsql
# instance.
# LIVE_SQLALCHEMY_DATABASE_URI = (
#     'mysql+pymysql://{user}:{password}@/{database}'
#     '?unix_socket=/cloudsql/{connection_name}').format(
#         user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
#         database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

# if os.environ.get('GAE_INSTANCE'):
# if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
#     SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
# else:
#     SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI
