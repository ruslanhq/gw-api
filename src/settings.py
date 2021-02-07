from typing import Any

from pydantic import HttpUrl, Field, AnyUrl, BaseConfig
from pydantic.fields import ModelField

from src.vault_backend import VaultBaseSettings


class MySQLDSN(AnyUrl):
    allowed_schemes = {'mysql', 'mysql+mysqldb', 'mysql+pymysql'}
    user_required = True

    def validate(
            cls,
            value: Any,
            field: 'ModelField',
            config: 'BaseConfig'
    ) -> 'AnyUrl':
        # fetch value from VAULT
        return super().validate('test', field=field, config=config)


class Configuration(VaultBaseSettings):
    DEBUG: bool = False
    VERSION: str = '0.0.1'
    PROJECT_NAME: str = 'gw-api'
    CONN_LIMIT: int = Field(
        ...,
        vault_secret_key='conn_limit',
        vault_secret_path='config/limits',
    )
    DATABASE_URI: MySQLDSN

    class Config:
        vault_ldap_login = 'vault'
        vault_ldap_password = 'test_password'
        vault_url: HttpUrl = 'http://vault.tld'
        vault_namespace: str = 'gateway/settings'
        vault_secret_mount_point: str = 'secrets'
