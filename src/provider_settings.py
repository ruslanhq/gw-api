import hvac
from sitri.providers.contrib.json import JsonConfigProvider
from sitri.providers.contrib.system import SystemConfigProvider
from sitri.providers.contrib.vault import VaultKVConfigProvider

configurator = SystemConfigProvider(prefix='GW_API')
ENV = configurator.get('env')
is_local_mode = ENV is None


def vault_client_factory() -> hvac.Client:
    client = hvac.Client(url=configurator.get('vault_api'))

    client.auth.approle.login(
        role_id=configurator.get('role_id'),
        secret_id=configurator.get('secret_id'),
    )

    return client


provider = VaultKVConfigProvider(
    vault_connector=vault_client_factory,
    mount_point=f"{configurator.get('app_name')}/settings",
) if not is_local_mode else JsonConfigProvider('./local_config.json')
