import requests
from typing import Union
from chainwebpy.url import (
    GenericNodeAPIEndpoint,
    P2PBootstrapAPIEndpoint,
    ServiceAPIEndpoint,
)
import json
from typing import List


class BlockHeaderEndpoints:
    """These endpoints return block headers from the chain database.

    Generally, block headers are returned in ascending order and include headers of orphaned blocks.

    For only querying blocks that are included in the winning branch of the chain the branch endpoints can be used, which return blocks in descending order starting from the leafs of branches of the block chain.

    """

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

    def get_block_headers(
        self,
        chain: int,
        limit: int = None,
        next: str = None,
        minheight: int = None,
        maxheight: int = None,
        responseSchema: str = "object",
    ):
        """A page of a collection of block headers in ascending order that satisfies query parameters. Any block header from the chain database is returned. This includes headers of orphaned blocks.

        Args:
            `chain` (int): The id of the chain to which the request is sent.
            `limit` (int, optional): Maximum number of records that may be returned. The actual number may be lower. Defaults to None.
            `next` (str, optional): The cursor for the next page. This value can be found as value of the next property of the previous page. Defaults to None.
            `minheight` (int, optional): Minimum block height of the returned headers. Defaults to None.
            `maxheight` (int, optional): Maximum block height of the returned headers. Defaults to None.
            `responseScheme` (str, optional): Response scheme. Can be one of "object", or "base64url". Defaults to "object".

        Raises:
            `TypeError`: If chain is not an integer or lower and upper values are not list of strings. Also if limit, next, minheight, or maxheight arguments are provided, they must be valid types.
            `ValueError`: If chain is less than 0 or responseScheme is not one of "object" or "base64url". Also if limit, next, minheight, or maxheight arguments are provided, they must be valid values.
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

        if minheight is not None:
            if not isinstance(minheight, int):
                raise TypeError("minheight must be an integer")

            elif minheight < 0:
                raise ValueError("minheight must be greater than 0")
            _payload["minheight"] = minheight

        if maxheight is not None:
            if not isinstance(maxheight, int):
                raise TypeError("maxheight must be an integer")

            elif maxheight < 0:
                raise ValueError("maxheight must be greater than 0")
            _payload["maxheight"] = maxheight

        if responseSchema not in ["object", "base64url"]:
            raise ValueError(
                "responseScheme must be one of 'object' or 'base64url'"
            )

        _headers = {"Content-type": "application/json"}

        if responseSchema == "binary":
            _headers["Accept"] = "application/json"

        elif responseSchema == "object":
            _headers["Accept"] = "application/json;blockheader-encoding=object"

        else:
            raise ValueError(
                "responseScheme must be one of 'object' or 'binary'"
            )

        _payload["chain"] = chain
        _endpoint = self.node.endpoint + f"/chain/{chain}/header"
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")
        return r.json()

    def get_block_headers_by_hash(
        self, chain: int, blockHash: str, responseSchema: str = "object"
    ):
        """Query a block header by its hash.

        Args:
            `chain` (int): The id of the chain to which the request is sent.
            `blockHash` (str): Block hash of a block.
            `responseScheme` (str, optional): Response scheme. Can be one of "object", "base64url", or "binary". Defaults to "object".

        Raises:
            `TypeError`: If chain is not an integer or blockHash is not a string.
            `ValueError`: If chain is less than 0 or responseScheme is not one of "object", "base64url", or "binary".
            `Exception`: If the request fails.
        """
        _payload = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")

        elif chain < 0:
            raise ValueError("chain must be greater than 0")

        if not isinstance(blockHash, str):
            raise TypeError("blockHash must be a string")

        if responseSchema not in ["object", "base64url", "binary"]:
            raise ValueError(
                "responseScheme must be one of 'object', 'base64url', or 'binary'"
            )

        _headers = {"Content-type": "application/json"}

        if responseSchema == "object":
            _headers["Accept"] = "application/json;blockheader-encoding=object"

        elif responseSchema == "base64url":
            _headers["Accept"] = "application/json"

        elif responseSchema == "binary":
            _headers["Accept"] = "application/octet-stream"

        _payload["chain"] = chain
        _payload["blockHash"] = blockHash
        _endpoint = self.node.endpoint + f"/chain/{chain}/header/{blockHash}"
        r = requests.get(_endpoint, params=_payload, headers=_headers)

        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")
        if responseSchema == "binary":
            return r.content

        return r.json()

    def get_block_header_branches(
        self,
        chain: int,
        lower: List[str],
        upper: List[str],
        limit: int = None,
        next: str = None,
        minHeight: int = None,
        maxHeight: int = None,
    ):
        """A page of block headers from branches of the block chain in descending order.

        Only blocks are returned that are ancestors of the some block in the set of upper bounds and are not ancestors of any block in the set of lower bounds.


                Args:
                    `chain` (int): The id of the chain to which the request is sent.
                    `lower` (List[str]): Array of strings (Block Hash). No blocks are returned that are predecessors of any block with an hash from this array.
                    `upper` (List[str]): Array of strings (Block Hash). Returned block headers are predecessors of a block with an hash from this array. This includes blocks with hashes from this array.
                    `limit` (int, optional): Maximum number of records that may be returned. The actual number may be lower. Defaults to None.
                    `next` (str, optional): The cursor for the next page. This value can be found as value of the next property of the previous page. Defaults to None.
                    `minHeight` (int, optional): Minimum block height of the returned headers. Defaults to None.
                    `maxHeight` (int, optional): Maximum block height of the returned headers. Defaults to None.

                Raises:
                    `TypeError`: If chain is not an integer or lower and upper values are not list of strings.
                    `ValueError`: If chain is less than 0.
                    `Exception`: If the request fails.
        """
        _payload = {}
        _data = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")

        elif chain < 0:
            raise ValueError("chain must be greater than 0")

        if not isinstance(lower, list):
            raise TypeError("lower must be a list of strings")

        if not isinstance(upper, list):
            raise TypeError("upper must be a list of strings")

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

        if minHeight is not None:
            if not isinstance(minHeight, int):
                raise TypeError("minHeight must be an integer")

            elif minHeight < 0:
                raise ValueError("minHeight must be greater than 0")
            _payload["minHeight"] = minHeight

        if maxHeight is not None:
            if not isinstance(maxHeight, int):
                raise TypeError("maxHeight must be an integer")

            elif maxHeight < 0:
                raise ValueError("maxHeight must be greater than 0")
            _payload["maxHeight"] = maxHeight

        _endpoint = self.node.endpoint + f"/chain/{chain}/header/branch"

        _headers = {"Content-type": "application/json"}
        _data["lower"] = lower
        _data["upper"] = upper
        r = requests.post(
            _endpoint, params=_payload, headers=_headers, data=json.dumps(_data)
        )
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")
        return r.json()
