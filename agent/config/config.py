from mutablesecurity.config import (
    ConfigurationKey,
    GenericConfigurationManager,
)
from mutablesecurity.helpers.data_type import IntegerDataType, StringDataType


class ConfigurationManager(GenericConfigurationManager):
    """Class defining the configuration used in MutableSecurity."""

    KEYS = [
        ConfigurationKey(
            "bind_address",
            StringDataType,
            default_value="0.0.0.0",  # noqa: S104
        ),
        ConfigurationKey(
            "bind_port",
            IntegerDataType,
            default_value=40400,
        ),
        ConfigurationKey(
            "email",
            StringDataType,
            default_value=False,
        ),
        ConfigurationKey(
            "password",
            StringDataType,
            default_value=False,
        ),
    ]
    FILENAME = ".mutablesecurity"

    def __init__(self) -> None:
        super().__init__(
            ConfigurationManager.KEYS, ConfigurationManager.FILENAME
        )
