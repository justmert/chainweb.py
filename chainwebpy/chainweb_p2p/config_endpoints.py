import requests
from typing import Union
from chainwebpy.url import (
    GenericNodeAPIEndpoint,
    P2PBootstrapAPIEndpoint,
    ServiceAPIEndpoint,
)


class ConfigEndpoints:
    def __init__(
        self,
        api: Union[
            GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint
        ],
    ):
        self.node = api

    def set_node_endpoint(
        self,
        api: Union[
            GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint
        ],
    ):
        """Set the node url that serves endpoints.

        Args:
            `api` (Union[GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint]): The node url that serves endpoints.
        """
        self.node = api

    def get_config(self):
        """Get the configuration of the node.

        Raises:
            `Exception`: If the request fails.
        """
        _endpoint = self.node.endpoint + "/config"

        _headers = {"Content-type": "application/json"}
        r = requests.get(_endpoint, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")
        return r.json()
