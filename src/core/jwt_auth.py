import datetime

import jwt
from fastapi import Header

from src.main import settings


class JwtUser:

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': (
                        datetime.datetime.utcnow() +
                        datetime.timedelta(days=0, seconds=30)
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                settings.SECRET_KEY.get_secret_value(),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def get_jwt_user(self, authorization: str = Header(...)):
        auth_token = authorization.split(" ")[1]
        try:
            payload = jwt.decode(auth_token,
                                 settings.SECRET_KEY.get_secret_value())
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise ValueError('Signature expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise ValueError('Invalid token. Please log in again.')
