import requests
from typing import Union
from kadenapy.url import (
    GenericNodeAPIEndpoint,
    P2PBootstrapAPIEndpoint,
    ServiceAPIEndpoint,
)


class PeerEndpoints:
    """The P2P communication between chainweb-nodes is sharded into several independent P2P network. The cut network is exchanging consensus state. There is also one mempool P2P network for each chain."""

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

    def get_cut_network_peer_info(
        self, limit: int = None, next: str = None
    ) -> dict:
        """Get cut-network peer info.

        Args:
            `limit` (int, optional): Maximum number of records that may be returned. The actual number may be lower. Defaults to None.
            `next` (str, optional): The cursor for the next page. This value can be found as value of the next property of the previous page. Defaults to None.

        Raises:
            `TypeError`: If limit or next is provided, then must be valid types.
            `ValueError`: If limit or next is provided, then must be valid values.
            `Exception`: If the request fails.
        """
        _payload = {}
        if limit is not None:
            if not isinstance(limit, int):
                raise TypeError("limit must be an integer")

            elif limit < 0:
                raise ValueError("limit must be greater than 0")

            _payload["limit"] = limit

        if next is not None:
            if not isinstance(next, str):
                raise TypeError("next must be a string")

            _payload["next"] = next

        _endpoint = self.node.endpoint + "/cut/peer"
        _headers = {"Content-type": "application/json"}
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")
        return r.json()

    def get_chain_mempool_network_peer_info(
        self, chain: int, limit: int = None, next: str = None
    ) -> dict:
        """Get chain mempool network peer info.

        Args:
            `chain` (int): The id of the chain to which the request is sent.
            `limit` (int, optional): Maximum number of records that may be returned. The actual number may be lower. Defaults to None.
            `next` (str, optional): The cursor for the next page. This value can be found as value of the next property of the previous page. Defaults to None.

        Raises:
            `TypeError`: If chain is not an integer. If limit or next is provided, then must be valid types.
            `ValueError`: If chain is less than 0. If limit or next is provided, then must be valid values.
            `Exception`: If the request fails.
        """
        _payload = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")

        elif chain < 0:
            raise ValueError("chain must be greater than 0")

        if limit is not None:
            if not isinstance(limit, int):
                raise TypeError("limit must be an integer")

            elif limit < 0:
                raise ValueError("limit must be greater than 0")
            _payload["limit"] = limit

        if next is not None:
            if not isinstance(next, str):
                raise TypeError("next must be a string")
            _payload["next"] = next

        _endpoint = self.node.endpoint + f"/chain/{chain}/mempool/peer"
        _headers = {"Content-type": "application/json"}
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")
        return r.json()
