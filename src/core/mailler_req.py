import hashlib
import hmac
from urllib.parse import urljoin

from src.core.http_requests import MakeRequest
from src.settings import settings
from src.core.enums import MaillerTemplateEnum


class SendMail:
    def __init__(self, username, mail, template_name, subject, payload):
        self.username = username
        self.mail = mail
        self.template_name = template_name
        self.subject = subject
        self.payload = payload
        self.url = urljoin(settings.mailler.url, 'mailler')
        self.check_payload()

    def check_payload(self):
        valid_keys = MaillerTemplateEnum[self.template_name].value
        missed_keys = \
            [key for key in valid_keys if key not in self.payload.keys()]
        if missed_keys:
            raise ValueError(
                'Payload keys are not valid, missed keys: ' +
                ", ".join(missed_keys)
            )

    async def request_to_mailler(self):
        return await MakeRequest(
            uri=self.url, method='POST', data=self.get_query
        ).do_request()

    @property
    def get_query(self) -> dict:
        return self._add_mac_signature(
            {
                "Mail": self.mail,
                "UserName": self.username,
                "TemplateName": self.template_name,
                "Subject": self.subject,
                "Payload": self.payload
            }
        )

    @staticmethod
    def _add_mac_signature(query: dict) -> dict:
        # Create string for mac
        str_query = []
        for (key, value) in query.items():
            if key == 'Payload':
                for (pl_key, pl_value) in value.items():
                    str_query.append(f'{pl_key}={pl_value}')
            else:
                str_query.append(f'{key}={value}')
        str_query.sort()
        str_query = '-'.join(str_query) + ';'
        # Create mac signature and add to dict
        mac = hmac.new(
            key=bytes(
                settings.mailler.key_mac_sign.get_secret_value(),
                encoding='utf8'
            ),
            msg=bytes(str_query, encoding='utf8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        query['mac'] = mac
        return query
