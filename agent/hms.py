import click
from agent.mutablesecurity.cli.printer import Printer
from agent.mutablesecurity.helpers.exceptions import MutableSecurityException
from rich.console import Console

from agent.hosts_manager import HostsManager

console = Console()
printer = Printer(console)
hosts_manager = HostsManager()


@click.group()
def cli() -> None:
    """Manages the hosts connected to the orchestration agent.

    The hosts are identified by an unique API key, automatically generated by
    this CLI tool.
    """


@cli.command()
@click.option("--identifier", required=True, help="Unique host identifier")
@click.option("--description", required=True, default="", help="Description")
def enroll(identifier: str, description: str) -> None:
    """Enroll a new host."""
    host = hosts_manager.enroll_host(identifier, description)
    hosts_manager.save_to_file()

    text = f'The key "{host.api_key}" was successfully created.'
    printer.print_success_message(text)


@cli.command()
@click.option("--identifier", required=True, help="Host identifier")
def delete(identifier: str) -> None:
    """Delete an enrolled host from database."""
    hosts_manager.delete_host(identifier)
    hosts_manager.save_to_file()

    text = f'The host "{identifier}" was successfully deleted.'
    printer.print_success_message(text)


@cli.command()
@click.option("--key", required=True, help="Key to verify")
def check(key: str) -> None:
    """Checks if a key is in the database."""
    is_present = hosts_manager.is_key_valid(key)

    if is_present:
        text = f'The key "{key}" is present in database.'
        printer.print_success_message(text)
    else:
        text = f'The key "{key}" is not present in database.'
        printer.print_error_message(text)


@cli.command()
def get() -> None:
    """Prints the content of the database."""
    entries = hosts_manager.get_all_hosts_as_matrix()

    headers = ["Identifier", "Description", "API Key"]
    entries.insert(0, headers)

    printer.print_table(entries)


def main() -> None:
    try:
        cli(standalone_mode=False)  # pylint: disable=no-value-for-parameter
    except MutableSecurityException as exception:
        printer.print_exception(exception)


if __name__ == "__main__":
    cli()
