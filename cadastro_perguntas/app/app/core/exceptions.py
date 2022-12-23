from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status


class InvalidUser(AuthenticationFailed):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = ("Credentials is invalid or didn't match")
    default_code = 'user_credentials_not_valid'
    
    
class InactiveUser(AuthenticationFailed):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = ("Credentials is invalid or didn't match")
    default_code = 'user_inactive'