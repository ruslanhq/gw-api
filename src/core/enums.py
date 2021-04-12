from enum import Enum


class HTTPErrorEnum(str, Enum):
    instance_not_found = '%s not found'.capitalize()


class MaillerTemplateEnum(Enum):
    welcome = ['company', 'date']
    reset_password = ['password', 'recovery_link']
