from typing import Optional

from pydantic import Field, AnyUrl, SecretStr, BaseModel
from sitri.settings.contrib.vault import VaultKVSettings

from src.provider_settings import provider, configurator


class MySQLDSN(AnyUrl):
    allowed_schemes = {'mysql', 'mysql+mysqldb', 'mysql+pymysql'}
    user_required = True


class DBSettings(BaseModel):
    dsn: MySQLDSN = Field(
        vault_secret_key='mysql_dsn',
        default='mysql+pymysql://root:root@localhost:3306/test'
    )

    class Config(VaultKVSettings.VaultKVSettingsConfig):
        provider = provider
        default_secret_path = 'db'


class AirFlowSettings(BaseModel):
    url: AnyUrl = Field(default='http://airflow', vault_secret_key='host')
    login: str = Field(default='', vault_secret_key='login')
    password: SecretStr = Field(default=None, vault_secret_key='password')

    class Config(VaultKVSettings.VaultKVSettingsConfig):
        provider = provider
        default_secret_path = 'airflow'


class KafkaSettings(BaseModel):
    mechanism: str = Field(
        default='SASL_PLAINTEXT',
        vault_secret_key='auth_mechanism'
    )
    brokers: str = Field(
        default='kafka:9092',
        vault_secret_key='brokers_url'
    )

    class Config(VaultKVSettings.VaultKVSettingsConfig):
        provider = provider
        default_secret_path = 'kafka'


class Configuration(BaseModel):
    DEBUG: bool = False
    VERSION: str = '0.0.1'
    PROJECT_NAME: str = 'gw-api'
    SECRET_KEY: Optional[SecretStr] = Field(
        default=None, vault_secret_key='secret_key'
    )

    database: Optional[DBSettings] = Field(default_factory=DBSettings)
    kafka: Optional[KafkaSettings] = Field(default_factory=KafkaSettings)
    airflow: Optional[AirFlowSettings] = Field(default_factory=AirFlowSettings)

    CONN_LIMIT: int = Field(default=0, vault_secret_key='conn_limit')

    class Config(VaultKVSettings.VaultKVSettingsConfig):
        provider = provider
        default_secret_path = 'settings'
        default_mount_point = f"{configurator.get('app_name')}/settings"
