import jwt
import datetime
from django.conf import settings
from api.models import UserMaster

def generate_access_token(user):
    access_token_payload = {
        'user_id': user,
        'username':UserMaster.objects.filter(id=user).last().username,
        'token_type': 'access',
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
        'jti': "b932ba39d8024b39a55b3850129cbd10"}
    return jwt.encode(access_token_payload,settings.SECRET_KEY, algorithm='HS256')


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user,
        'username':UserMaster.objects.filter(id=user).last().username,
        'token_type': 'refresh',
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=4),
        'jti': "b932ba39d8024b39a55b3850129cbd10"}
    return jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')


