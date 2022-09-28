from enum import Enum
from typing import Union


class GenericNodeAPIEndpoint(object):
    """The generic node API endpoint.

    Args:
        `scheme` (str): The scheme of the node url.
        `domain` (str): The domain of the node url.
        `port` (int): The port of the node url.
        `api_version` (str): The API version of the node url.
        `chainweb_version` (str): The Chainweb version of the node url.

    """

    def __init__(
        self,
        scheme: str,
        domain: str,
        port: int,
        api_version: str,
        chainweb_version: str,
    ):
        self.node_host = f"{scheme}://{domain}:{port}"
        self.node_endpoint = (
            f"{self.node_host}/chainweb/{api_version}/{chainweb_version}"
        )

    @property
    def endpoint(self) -> str:
        return self.node_endpoint

    @property
    def host(self) -> str:
        return self.node_host


class P2PBootstrapAPIEndpoint(object):
    """Chainweb P2P bootstrap node. Only P2P API endpoints are served.

    Args:
        `location` (Union[MainnetNode, TestnetNode]): The location of the node url.
        `api_version` (str): The API version of the node url.

    Raises:
        ValueError: If `location` is not one of `MainnetNode`, `TestnetNode`.
    """

    class TestnetNode(Enum):
        """Chainweb testnet P2P bootstrap node list. Only P2P API endpoints are served."""

        US1 = "us1"
        US2 = "us2"
        EU1 = "eu1"
        EU2 = "eu2"
        AP1 = "ap1"
        AP2 = "ap2"

    class MainnetNode(Enum):
        """Chainweb mainnet P2P bootstrap node list. Only P2P API endpoints are served."""

        US_E1 = "us-e1"
        US_E2 = "us-e2"
        US_E3 = "us-e3"
        US_W1 = "us-w1"
        US_W2 = "us-w2"
        US_W3 = "us-w3"
        JP1 = "jp1"
        JP2 = "jp2"
        JP3 = "jp3"
        FR1 = "fr1"
        FR2 = "fr2"
        FR3 = "fr3"

    def __init__(
        self,
        location: Union[MainnetNode, TestnetNode],
        api_version: str = "0.0",
    ):
        if isinstance(location, self.MainnetNode):
            self.node_host = f"https://{location.value}.chainweb.com"
            self.node_endpoint = (
                f"{self.node_host}/chainweb/{api_version}/mainnet01"
            )

        elif isinstance(location, self.TestnetNode):
            self.node_host = f"https://{location.value}.testnet.chainweb.com"
            self.node_endpoint = (
                f"{self.node_host}/chainweb/{api_version}/testnet04"
            )

        else:
            raise ValueError(
                "Invalid location. Must be one of 'MainnetNode', 'TestnetNode' or 'str'"
            )

    @property
    def endpoint(self) -> str:
        return self.node_endpoint

    @property
    def host(self) -> str:
        return self.node_host


class ServiceAPIEndpoint(object):
    """Chainweb mainnet or testnet service API. It also serves some endpoints of the P2P API.

    Args:
        `network` (str): Chainweb network. Must be one of 'testnet' or 'mainnet'. Defaults to 'testnet'.
    """

    def __init__(self, network: str = "testnet"):
        if network.lower() == "testnet":
            self.node_host = "https://api.testnet.chainweb.com"
            self.node_endpoint = f"{self.node_host}/chainweb/0.0/testnet04"

        elif network.lower() == "mainnet":
            self.node_host = "https://api.chainweb.com"
            self.node_endpoint = f"{self.node_host}/chainweb/0.0/mainnet01"

        else:
            raise ValueError(
                "Invalid network. Must be one of 'testnet' or 'mainnet'"
            )

    @property
    def endpoint(self) -> str:
        return self.node_endpoint

    @property
    def host(self) -> str:
        return self.node_host
