from mutablesecurity.helpers.exceptions import MutableSecurityException


class HostsManagementException(MutableSecurityException):
    """An error occurred in the management of hosts."""


class KeyNotPresentException(HostsManagementException):
    """The key is not present in the database."""


class InvalidKeyPresentInFileException(HostsManagementException):
    """An API key present in the local database is invalid."""


class IdentifierAlreadyPresentException(HostsManagementException):
    """The given identifier is already present."""


class ServerException(MutableSecurityException):
    """An error occurred in the main module."""


class InvalidAPIKeyUsedException(ServerException):
    """The API key that was used in the request is invalid."""
