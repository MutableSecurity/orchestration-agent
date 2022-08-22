import typing

from flask import Flask, request
from werkzeug.exceptions import BadRequest, HTTPException, Unauthorized

from agent.config import ConfigurationManager
from agent.helpers.exceptions import InvalidAPIKeyUsedException
from agent.server import Server

FlaskResponse = typing.Union[str, HTTPException]


flask = Flask(__name__)
server = Server()

ORCHESTRATOR_REPORT_ROUTE = "/report"


@flask.route(ORCHESTRATOR_REPORT_ROUTE, methods=["POST"])
def hello_world() -> FlaskResponse:
    raw_data = request.get_json(silent=True)
    if raw_data is None:
        return BadRequest()

    api_key = raw_data.get("api_key", None)
    data = raw_data.get("data", None)
    if api_key is None or data is None:
        return BadRequest()

    try:
        server.report_data(api_key, data)
    except InvalidAPIKeyUsedException:
        return Unauthorized()

    return ""


def main() -> None:
    config_manager = ConfigurationManager()

    flask.run(
        host=config_manager.bind_address,
        port=config_manager.bind_port,
        ssl_context="adhoc",
    )


if __name__ == "__main__":
    main()
