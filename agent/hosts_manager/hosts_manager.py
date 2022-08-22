import string
import typing

from mutablesecurity.helpers.exceptions import YAMLFileNotExistsException
from mutablesecurity.helpers.type_hints import StringMatrix
from mutablesecurity.helpers.yaml_parser import dump_to_file, load_from_file

from agent.helpers.exceptions import (
    IdentifierAlreadyPresentException,
    InvalidKeyPresentInFileException,
    KeyNotPresentException,
)
from agent.hosts_manager.api_key import (
    generate_random_key,
    has_key_valid_format,
)


class EnrolledHost:
    identifier: str
    description: str
    api_key: str

    def __init__(
        self, identifier: str, description: str, api_key: str
    ) -> None:
        self.identifier = identifier
        self.description = description
        self.api_key = api_key

    def to_list(self) -> typing.List[str]:
        return [self.identifier, self.description, self.api_key]

    def to_dict(self) -> dict:
        return self.__dict__


class HostsManager:
    ALPHABET = string.ascii_letters + string.digits
    DATABASE_LOCATION = ".hosts"
    KEY_LENGTH = 64

    hosts: typing.List[EnrolledHost]

    def __init__(self) -> None:
        try:
            content = load_from_file(self.DATABASE_LOCATION, is_plain=False)
        except YAMLFileNotExistsException:
            self.hosts = []
        else:
            self.hosts = [
                EnrolledHost(**details) for details in content["hosts"]
            ]

        self.__validate_hosts()

    def __validate_hosts(self) -> None:
        for host in self.hosts:
            self.__validate_single_host(host)

    def __validate_single_host(self, host: EnrolledHost) -> None:
        if not has_key_valid_format(
            host.api_key, self.ALPHABET, self.KEY_LENGTH
        ):
            raise InvalidKeyPresentInFileException()

    def is_key_valid(self, key: str) -> bool:
        for host in self.hosts:
            if host.api_key == key:
                return True

        return False

    def enroll_host(self, identifier: str, description: str) -> EnrolledHost:
        if self.__is_host_present(identifier):
            raise IdentifierAlreadyPresentException()

        key = generate_random_key(self.ALPHABET, self.KEY_LENGTH)

        host = EnrolledHost(identifier, description, key)
        self.hosts.append(host)

        return host

    def __is_host_present(self, identifier: str) -> bool:
        return any([host.identifier == identifier for host in self.hosts])

    def delete_host(self, identifier: str) -> None:
        initial_length = len(self.hosts)

        self.hosts = [
            host for host in self.hosts if host.identifier != identifier
        ]
        length_after_removal = len(self.hosts)

        if initial_length == length_after_removal:
            raise KeyNotPresentException()

    def save_to_file(self) -> None:
        hosts_dict = [host.to_dict() for host in self.hosts]
        content = {"hosts": hosts_dict}

        dump_to_file(content, self.DATABASE_LOCATION, is_plain=False)

    def get_all_hosts_as_matrix(self) -> StringMatrix:
        return [host.to_list() for host in self.hosts]
