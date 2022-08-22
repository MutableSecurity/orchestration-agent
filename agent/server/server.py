from agent.config import ConfigurationManager
from agent.helpers.exceptions import InvalidAPIKeyUsedException
from agent.hosts_manager import HostsManager
from agent.storage import Storage


class Server:
    configuration: ConfigurationManager
    hosts_manager: HostsManager
    storage: Storage

    def __init__(self) -> None:
        self.configuration = ConfigurationManager()
        self.hosts_manager = HostsManager()

        self.__init_storage()

    def __init_storage(self) -> None:
        email = self.configuration.email
        password = self.configuration.password

        self.storage = Storage(email, password)

    def report_data(self, api_key: str, data: dict) -> None:
        if not self.hosts_manager.is_key_valid(api_key):
            raise InvalidAPIKeyUsedException()

        self.storage.store_data(data)
