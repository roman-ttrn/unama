from rest_framework.authentication import TokenAuthentication 
from rest_framework.authtoken.models import Token

class TokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'
