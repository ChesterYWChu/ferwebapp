try:
    from functools import lru_cache
except ImportError:
    from functools32 import lru_cache
# [START rest_writing_data]
import json
import httplib2
from oauth2client.client import GoogleCredentials
import logging

logger = logging.getLogger('')

_FIREBASE_SCOPES = [
    'https://www.googleapis.com/auth/firebase.database',
    'https://www.googleapis.com/auth/userinfo.email']

@lru_cache()
def _get_http():
    """Provides an authed http object."""
    http = httplib2.Http()
    # Use application default credentials to make the Firebase calls
    # https://firebase.google.com/docs/reference/rest/database/user-auth
    creds = GoogleCredentials.get_application_default().create_scoped(
        _FIREBASE_SCOPES)
    creds.authorize(http)
    return http


# dev_appserver.py --appidentity_email_address fer-owner-account@fer-project-170115.iam.gserviceaccount.com --appidentity_private_key_path /Users/yourway_chu/Downloads/secret.pem --port=9999 --default_gcs_bucket_name fer-app-engine app.yaml


def firebase_put(path, value=None):
    """Writes data to Firebase.

    An HTTP PUT writes an entire object at the given database path. Updates to
    fields cannot be performed without overwriting the entire object

    Args:
        path - the url to the Firebase object to write.
        value - a json string.
    """
    response, content = _get_http().request(path, method='PUT', body=value)
    logger.info(content)
    return json.loads(content)

def firebase_patch(path, value=None):
    """Update specific children or fields
    An HTTP PATCH allows specific children or fields to be updated without
    overwriting the entire object.
    Args:
        path - the url to the Firebase object to write.
        value - a json string.
    """
    response, content = _get_http().request(path, method='PATCH', body=value)
    logger.debug(content)
    return json.loads(content)

def firebase_get(path):
    """Read the data at the given path.

    An HTTP GET request allows reading of data at a particular path.
    A successful request will be indicated by a 200 OK HTTP status code.
    The response will contain the data being retrieved.

    Args:
        path - the url to the Firebase object to read.
    """
    response, content = _get_http().request(path, method='GET')
    logger.debug(content)
    return json.loads(content)












# import sys

# class dummy:
#     def close(self):
#         pass
#     def join(self):
#         pass
#     def terminate(self):
#         pass

# class DummyProccessing():
#     def __init__(self):
#         pass
#     @staticmethod
#     def Pool(processes):
#         return dummy()

# sys.modules['firebase.async.process_pool'] = dummy()
# sys.modules['multiprocessing'] = DummyProccessing

# from firebase import firebase
# import logging

# logger = logging.getLogger('')

# firebase = firebase.FirebaseApplication('https://fer-project-170115.firebaseio.com/', None)

# new_user = 'Ozgur Vatansever'
# result = firebase.post('/users', new_user)
# logger.info(result)

# result = firebase.get('/users', None)
# logger.info(result)
