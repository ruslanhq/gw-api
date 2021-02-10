from pydantic import Field, AnyUrl
from sitri.settings.contrib.vault import VaultKVSettings

from src.provider_settings import provider, configurator


class MySQLDSN(AnyUrl):
    allowed_schemes = {'mysql', 'mysql+mysqldb', 'mysql+pymysql'}
    user_required = True


class DBSettings(VaultKVSettings):
    dsn: MySQLDSN = Field(..., vault_secret_key="mysql_dsn")

    class Config(VaultKVSettings.VaultKVSettingsConfig):
        provider = provider
        default_secret_path = "db"


class KafkaSettings(VaultKVSettings):
    mechanism: str = Field(..., vault_secret_key="auth_mechanism")
    brokers: str = Field(...)

    class Config(VaultKVSettings.VaultKVSettingsConfig):
        provider = provider
        default_secret_path = "kafka"
        default_mount_point = f"{configurator.get('app_name')}/common"


class Configuration(VaultKVSettings):
    DEBUG: bool = False
    VERSION: str = '0.0.1'
    PROJECT_NAME: str = 'gw-api'

    database: DBSettings = Field(default_factory=DBSettings)
    kafka: KafkaSettings = Field(default_factory=KafkaSettings)

    CONN_LIMIT: int = Field(..., vault_secret_key='conn_limit')

    class Config(VaultKVSettings.VaultKVSettingsConfig):
        provider = provider
        default_secret_path = "settings"
        default_mount_point = f"{configurator.get('app_name')}/common"
