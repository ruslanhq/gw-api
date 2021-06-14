from typing import Optional

from pydantic import Field, AnyUrl, SecretStr, BaseModel
from sitri.settings.contrib.vault import VaultKVSettings

from src.provider_settings import provider, is_local_mode


class BaseSettingsConfig(VaultKVSettings.VaultKVSettingsConfig):
    provider = provider
    local_mode = is_local_mode
    local_provider_args = {"json_path": './local_config.json'}


class MySQLDSN(AnyUrl):
    allowed_schemes = {'mysql', 'mysql+aiomysql'}
    user_required = True


class DBSettings(VaultKVSettings):
    dsn: MySQLDSN = Field(
        vault_secret_key='mysql_dsn',
        default='mysql+aiomysql://root:root@localhost:3306/test'
    )

    class Config(BaseSettingsConfig):
        default_secret_path = 'db'
        local_mode_path_prefix = 'db'


class AirFlowSettings(VaultKVSettings):
    url: AnyUrl = Field(default='http://airflow', vault_secret_key='host')
    login: str = Field(default='', vault_secret_key='login')
    password: SecretStr = Field(default=None, vault_secret_key='password')

    class Config(BaseSettingsConfig):
        default_secret_path = 'airflow'
        local_mode_path_prefix = 'airflow'


class KafkaSettings(VaultKVSettings):
    mechanism: str = Field(
        default='SASL_PLAINTEXT',
        vault_secret_key='auth_mechanism'
    )
    brokers: str = Field(
        default='kafka:9092',
        vault_secret_key='brokers_url'
    )

    class Config(BaseSettingsConfig):
        default_secret_path = 'kafka'
        local_mode_path_prefix = 'kafka'


class MaillerSettings(VaultKVSettings):
    url: AnyUrl = Field(
        default=None, vault_secret_key='host'
    )
    key_mac_sign: SecretStr = Field(
        default=None, vault_secret_key='key_mac_sign'
    )

    class Config(BaseSettingsConfig):
        default_secret_path = 'mailler'
        local_mode_path_prefix = 'mailler'


class Main(VaultKVSettings):
    SECRET_KEY: Optional[SecretStr] = Field(
        default=None, vault_secret_key='secret_key'
    )
    SENTRY_DSN: Optional[AnyUrl] = Field(
        default=None, vault_secret_key='sentry_dsn',
    )

    class Config(BaseSettingsConfig):
        default_secret_path = 'main'


class Configuration(BaseModel):
    DEBUG: bool = False
    PAGE_SIZE: int = 20
    VERSION: str = '0.0.1'
    PROJECT_NAME: str = 'gw-api'

    database: Optional[DBSettings] = Field(default_factory=DBSettings)
    kafka: Optional[KafkaSettings] = Field(default_factory=KafkaSettings)
    airflow: Optional[AirFlowSettings] = Field(default_factory=AirFlowSettings)
    mailler: Optional[MaillerSettings] = Field(default_factory=MaillerSettings)
    main: Optional[Main] = Field(default_factory=Main)


settings = Configuration()

__all__ = ['settings']
