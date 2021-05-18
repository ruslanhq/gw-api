import datetime

import jwt

from src.settings import settings


class JwtUser:

    @staticmethod
    def encode_auth_token(user_id):
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
                settings.main.SECRET_KEY.get_secret_value(),
                algorithm='HS256'
            )
        except Exception as e:
            return e
