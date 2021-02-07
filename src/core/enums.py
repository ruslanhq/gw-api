from enum import Enum


class HTTPErrorEnum(str, Enum):
    instance_not_found = '%s not found'.capitalize()
