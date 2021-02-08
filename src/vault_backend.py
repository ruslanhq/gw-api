import logging
from pathlib import Path
from typing import Dict, Optional, Any, Union, ClassVar

import hvac
from hvac.exceptions import VaultError
from pydantic import BaseSettings, SecretStr, HttpUrl
from pydantic.env_settings import SettingsError
from pydantic.utils import deep_update
from typing_extensions import TypedDict


class HvacClientParameters(TypedDict, total=False):
    namespace: str
    token: str


class HvacReadSecretParameters(TypedDict, total=False):
    path: str
    mount_point: str


class VaultBaseSettings(BaseSettings):

    def _build_values(
            self,
            init_kwargs: Dict[str, Any],
            _env_file: Union[Path, str, None] = None,
            _env_file_encoding: Optional[str] = None,
            _secrets_dir: Union[Path, str, None] = None,
    ) -> Dict[str, Any]:
        return deep_update(
            deep_update(self._build_vault(), self._build_environ(_env_file)),
            init_kwargs,
        )

    def get_value_field(self, secret_params, secret_key) -> str:
        try:
            _config = self.__config__
            return _config.vault_client.secrets.kv.v2.read_secret_version(
                **secret_params
            )['data']['data'][secret_key]
        except VaultError:
            _secret_path = secret_params.get('path', 'unknown')
            logging.info(
                f'Could not get secret [{_secret_path}:{secret_key}]'
            )

    def _build_vault(self) -> Dict[str, Optional[str]]:
        d: Dict[str, Optional[str]] = {}

        # Login
        _config = self.__config__
        hvac_parameters: HvacClientParameters = {}
        if _config.vault_namespace is not None:
            hvac_parameters.update({
                'namespace': _config.vault_namespace
            })
        if _config.vault_token is not None:
            hvac_parameters.update({'token': _config.vault_token})

        if not _config.vault_token or not \
                (_config.vault_ldap_login and
                 _config.vault_ldap_password):
            assert 'Not configured auth hvac client'

        _config.vault_client = vault_client = hvac.Client(
            _config.vault_url, **hvac_parameters
        )

        if _config.vault_ldap_login and \
                _config.vault_ldap_password and \
                not _config.vault_token:
            vault_client.auth.ldap.login(
                username=_config.vault_ldap_login,
                password=_config.vault_ldap_password.get_secret_value(),
            )

        # Get secrets
        for field in self.__fields__.values():
            secret_key = field.field_info.extra.get('vault_secret_key')
            secret_path = field.field_info.extra.get('vault_secret_path')
            vault_secret_mount_point = _config.vault_secret_mount_point

            read_secret_parameters: dict = \
                HvacReadSecretParameters({'path': secret_path})
            if vault_secret_mount_point is not None:
                read_secret_parameters['mount_point'] = vault_secret_mount_point

            vault_val = self.get_value_field(read_secret_parameters, secret_key)

            if field.is_complex():
                try:
                    vault_val = _config.json_loads(vault_val)
                except ValueError as e:
                    raise SettingsError(
                        f'Error parsing JSON for [{secret_path}:{secret_key}]'
                    ) from e

            d[field.alias] = vault_val

        return d

    class Config(BaseSettings.Config):
        vault: ClassVar = None

        vault_url: HttpUrl
        vault_token: Optional[str]
        vault_ldap_login: Optional[str]
        vault_ldap_password: Optional[SecretStr]
        vault_namespace: Optional[str] = None
        vault_secret_mount_point: Optional[str] = None

    __config__: Config
