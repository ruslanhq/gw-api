import logging
from pathlib import Path
from typing import Dict, Optional, Any, Union

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
            self, init_kwargs: Dict[str, Any],
            _env_file: Union[Path, str, None] = None
    ) -> Dict[str, Any]:
        return deep_update(
            deep_update(self._build_vault(), self._build_environ(_env_file)),
            init_kwargs,
        )

    def _build_vault(self) -> Dict[str, Optional[str]]:
        d: Dict[str, Optional[str]] = {}

        # Login
        hvac_parameters: HvacClientParameters = {}
        if self.__config__.vault_namespace is not None:
            hvac_parameters.update({
                'namespace': self.__config__.vault_namespace
            })
        if self.__config__.vault_token is not None:
            hvac_parameters.update({'token': self.__config__.vault_token})

        if not self.__config__.vault_token or not \
                (self.__config__.vault_ldap_login and
                 self.__config__.vault_ldap_password):
            assert 'Not configured auth hvac client'

        vault_client = hvac.Client(
            self.__config__.vault_url, **hvac_parameters
        )

        if self.__config__.vault_ldap_login and \
                self.__config__.vault_ldap_password and \
                not self.__config__.vault_token:
            vault_client.auth.ldap.login(
                username=self.__config__.vault_ldap_login,
                password=self.__config__.vault_ldap_password.get_secret_value(),
            )

        # Get secrets
        for field in self.__fields__.values():
            vault_val: Optional[str] = None

            secret_key = field.field_info.extra['vault_secret_key']
            secret_path = field.field_info.extra['vault_secret_path']
            vault_secret_mount_point = self.__config__.vault_secret_mount_point

            read_secret_parameters: dict = \
                HvacReadSecretParameters({'path': secret_path})
            if vault_secret_mount_point is not None:
                read_secret_parameters['mount_point'] = vault_secret_mount_point

            try:
                vault_val = vault_client.secrets.kv.v2.read_secret_version(
                    **read_secret_parameters
                )['data']['data'][secret_key]
            except VaultError:
                logging.info(
                    f'Could not get secret [{secret_path}:{secret_key}]'
                )

            if field.is_complex():
                try:
                    vault_val = (
                        self.__config__.json_loads(vault_val)
                    )  # type: ignore
                except ValueError as e:
                    raise SettingsError(
                        f'Error parsing JSON for [{secret_path}:{secret_key}]'
                    ) from e

            d[field.alias] = vault_val

        return d

    class Config(BaseSettings.Config):
        vault_url: HttpUrl
        vault_token: Optional[str]
        vault_ldap_login: Optional[str]
        vault_ldap_password: Optional[SecretStr]
        vault_namespace: Optional[str] = None
        vault_secret_mount_point: Optional[str] = None

    __config__: Config
