from agent.mutablesecurity.config.config import (
    ConfigurationKey,
    ConfigurationManager as GenericConfigurationManager,
)
from agent.mutablesecurity.helpers.data_type import IntegerDataType, StringDataType

from enum import Enum

class ConfigurationManager(GenericConfigurationManager):
    class ConfigurationKeys(Enum):
        """Enumeration for all the keys from the configuration file."""

        BIND_ADDRESS = ConfigurationKey(
            "bind_address",
            StringDataType,
            default_value="0.0.0.0",  # noqa: S104
        )
        BIND_PORT = ConfigurationKey(
            "bind_port",
            IntegerDataType,
            default_value=40400,
        )
        EMAIL = ConfigurationKey(
            "email",
            StringDataType,
            default_value="",
        )
        PASSWORD = ConfigurationKey(
            "password",
            StringDataType,
            default_value="",
        )

    def __init__(self) -> None:
        super().__init__(
            ".mutablesecurity",
            ConfigurationManager, 
        )