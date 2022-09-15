from enum import Enum
from urllib.error import HTTPError
import requests
import urllib.parse
import typing
import chainweb.p2p_utils as p2p_utils
from typing import Any, Dict, List, Optional, Tuple, Union

class TestnetNode(Enum):
        """Chainweb testnet P2P bootstrap node list. Only P2P API endpoints are served."""
        US1 =  "us1"
        US2 =  "us2"
        EU1 =  "eu1"
        EU2 =  "eu2"
        AP1 =  "ap1"
        AP2 =  "ap2"

class MainnetNode(Enum):
        """Chainweb mainnet P2P bootstrap node list. Only P2P API endpoints are served."""
        US_E1 =  "us-e1"
        US_E2 =  "us-e2"
        US_E3 =  "us-e3"
        US_W1 =  "us-w1"
        US_W2 =  "us-w2"
        US_W3 =  "us-w3"
        JP1 =  "jp1"
        JP2 =  "jp2"
        JP3 =  "jp3"
        FR1 =  "fr1"
        FR2 =  "fr2"
        FR3 =  "fr3"


class ChainwebP2P():
    def __init__(self, api_version: int = "0.0", node: Union[TestnetNode, MainnetNode, str] = TestnetNode.US1) -> None:
        """The P2P API is used for inter-node communication in order to establish block chain consensus. 
        Each chainweb-node serves these endpoints via HTTPS on a network interface and port that is available directly on the public internet.

        Additionally, endpoints of the P2P API can be made available for other clients. 
        For this purpose it is possible to expose the endpoints via reverse proxies, load balancers, or authentication frameworks, and similar web technologies.

        Args:
            api_version (int, optional): Chainweb API version. Defaults to "0.0".
            node (Union[TestnetNode, MainnetNode, str], optional): Node P2P bootstrap node that serves P2P API endpoints. Can be instance of TestnetNode or MainnetNode. Defaults to TestnetNode.US1.
            Also can be string of form "{schema}://{domain}:{port}/chainweb/{apiVersion}/{chainwebVersion}".
        """
        self.node = None
        self.api_version = None
        self.set_api_endpoint(api_version, node)

    @property
    def get_api_endpoint(self):
        """Get the node endpoint.

        Returns:
            str: Node endpoint.
        """        
        return self._CHAINWEB_ENDPOINT

    @property
    def get_node_location(self):
        """Get the node location.

        Returns:
            str: Node location.
        """        
        return self.node

    def set_api_endpoint(self, api_version:int = "0.0", node: Union[TestnetNode, MainnetNode, str] = TestnetNode.US1) -> None:
        """Set the node endpoint.

        Args:
            api_version (int, optional): Chainweb API version. Defaults to "0.0".
            node (Union[TestnetNode, MainnetNode, str], optional): Node P2P bootstrap node that serves P2P API endpoints. Can be instance of TestnetNode or MainnetNode. Defaults to TestnetNode.US1.
            Also can be string of form "{schema}://{domain}:{port}/chainweb/{apiVersion}/{chainwebVersion}".
        """
        if isinstance(node, TestnetNode):
            endpoint = f"https://{node.value}.testnet.chainweb.com/chainweb/{api_version}/testnet04"
        elif isinstance(node, MainnetNode):
            endpoint = f"https://{node.value}.chainweb.com/chainweb/{api_version}/mainnet01"
        else:
            if node[-1] == '/':
                endpoint = node[:-1]
            else:
                endpoint = node

        self._CHAINWEB_ENDPOINT = endpoint
        self.node = node
        self.api_version = api_version

    def get_cut(self, maxheight: int=None) -> dict: # GET METHOD
        """Query the current cut from a Chainweb node.

        Args:
            maxheight (int, optional): Maximum cut height of the returned cut. Defaults to None.

        Raises:
            TypeError: If maxheight is not an integer.
            ValueError: If maxheight is less than 0.
            HTTPError: If the request fails.

        Returns:
            dict: Current cut from a Chainweb node.
        """                
        _payload = {}
        if maxheight is not None:
            if not isinstance(maxheight, int):
                raise TypeError("maxheight must be an integer")
            
            elif maxheight < 0:
                raise ValueError("maxheight must be greater than 0")
            _payload["maxheight"] = maxheight
        
        print(self._CHAINWEB_ENDPOINT)
        _endpoint = self._CHAINWEB_ENDPOINT + "/cut"
        _headers = {"Content-type": "application/json"}
        print(_endpoint)
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        return r.json()

    def get_block_hashes(self, chain: int, limit: int = None, next: str = None, minheight: int = None, maxheight: int = None) -> dict: # GET METHOD   
        """A page of a collection of block hashes in ascending order that satisfies query parameters.
        Any block hash from the chain database is returned. This includes hashes of orphaned blocks.

        Args:
            chain (int): The id of the chain to which the request is sent.
            limit (int, optional): Maximum number of records that may be returned. The actual number may be lower. Defaults to None.
            next (str, optional): The cursor for the next page. This value can be found as value of the next property of the previous page. Defaults to None.
            minheight (int, optional): Minimum block height of the returned headers. Defaults to None.
            maxheight (int, optional): Maximum block height of the returned headers. Defaults to None.

        Raises:
            TypeError: If chain is not an integer. Also if limit, next, minheight, or maxheight arguments are provided and are valid types.
            ValueError: If chain is less than 0. Also if limit, next, minheight, or maxheight arguments are provided and are valid values.
            HTTPError: If the request fails.
            
        Returns:
            dict: Array of block hashes
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
        
        _payload["chain"] = chain    
        _endpoint = self._CHAINWEB_ENDPOINT + f"/chain/{chain}/hash"
        _headers = {"Content-type": "application/json"}
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        return r.json()
        
    def get_block_headers(self, chain: int, limit: int = None, next: str = None, minheight: int = None, maxheight: int = None, responseSchema: str = "object") -> dict: # GET METHOD   
        """A page of a collection of block headers in ascending order that satisfies query parameters. 
        Any block header from the chain database is returned. This includes headers of orphaned blocks.


        Args:
            chain (int): The id of the chain to which the request is sent.
            limit (int, optional): Maximum number of records that may be returned. The actual number may be lower. Defaults to None.
            next (str, optional): The cursor for the next page. This value can be found as value of the next property of the previous page. Defaults to None.
            minheight (int, optional): Minimum block height of the returned headers. Defaults to None.
            maxheight (int, optional): Maximum block height of the returned headers. Defaults to None.
            responseScheme (str, optional): Response scheme. Can be one of "object", or "base64url". Defaults to "object".

        Raises:
            TypeError: If chain is not an integer. Also if limit, next, minheight, maxheight, or responseSchema arguments are provided, then must be valid types.
            ValueError: If chain is less than 0. Also if limit, next, minheight, maxheight, or responseSchema arguments are provided, then must be valid values.
            HTTPError: If the request fails.
            
        Returns:
            dict: Array of block hashes
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
            raise ValueError("responseScheme must be one of 'object' or 'base64url'")
        
        _headers = {"Content-type": "application/json"}        
        if responseSchema == "object":
            _headers = {"Content-type": "application/json;blockheader-encoding=object"}

        _payload["chain"] = chain    
        _endpoint = self._CHAINWEB_ENDPOINT + f"/chain/{chain}/header"

        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        return r.json()

    def get_block_headers_by_hash(self, chain: int, blockHash: str, responseSchema: str = "object") -> str: # GET METHOD
        """Query a block header by its hash.

        Args:
            chain (int): The id of the chain to which the request is sent.
            blockHash (str): Block hash of a block.
            responseScheme (str, optional): Response scheme. Can be one of "object", "base64url", or "binary". Defaults to "object".

        Raises:
            TypeError: If chain is not an integer or blockHash is not a string.
            ValueError: If chain is less than 0 or blockHash is not a valid base 64 url encoded string.
            HTTPError: If the request fails.

        Returns:
            str: Base64Url (without padding) encoded binary block header
        """                
        _payload = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(blockHash, str):
            raise TypeError("blockHash must be a string")
        
        elif not p2p_utils._isBase64(blockHash):
            raise ValueError("blockHash must be a valid base 64 string")

        if responseSchema not in ["object", "base64url", "binary"]:
            raise ValueError("responseScheme must be one of 'object', 'base64url', or 'binary'")

        
        _headers = {"Content-type": "application/json"}
        if responseSchema == "object":
            _headers = {"Content-type": "application/json;blockheader-encoding=object"}

        elif responseSchema == "binary":
            _headers = {"Content-type": "application/octet-stream"}

        _payload["chain"] = chain
        _payload["blockHash"] = blockHash

        _endpoint = self._CHAINWEB_ENDPOINT + f"/chain/{chain}/header/{blockHash}"
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        return r.json()

    def get_block_payload(self, chain: int, payloadHash: str) -> dict:
        """Get block payload.

        Args:
            chain (int): The id of the chain to which the request is sent.
            payloadHash (str): Payload hash of a block.

        Raises:
            TypeError: If chain is not an integer or payloadHash is not a string.
            ValueError: If chain is less than 0 or payloadHash is not a valid base 64 url encoded string.
            HTTPError: If the request fails.

        Returns:
            dict: Block payload.
        """                
        _payload = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(payloadHash, str):
            raise TypeError("payloadHash must be an string")
        
        elif not p2p_utils._isBase64(payloadHash):
            raise ValueError("payloadHash must be a valid base 64 string")

        _payload["chain"] = chain
        _payload["payloadHash"] = payloadHash

        _headers = {"Content-type": "application/json"}
        _endpoint = self._CHAINWEB_ENDPOINT + f"/chain/{chain}/payload/{payloadHash}"
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        return r.json()

    def get_payload_with_outputs(self, chain: int, payloadHash: str) -> dict:
        """Get block payload with outputs.

        Args:
            chain (int): The id of the chain to which the request is sent.
            payloadHash (str): Payload hash of a block.

        Raises:
            TypeError: if chain is not an integer or payloadHash is not a string.
            ValueError: if chain is less than 0 or payloadHash is not a valid base 64 url encoded string.
            HTTPError: if the request fails.

        Returns:
            dict: Block payload with outputs.
        """                
        _payload = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(payloadHash, str):
            raise TypeError("payloadHash must be an string")
        
        elif not p2p_utils._isBase64(payloadHash):
            raise ValueError("payloadHash must be a valid base 64 string")

        _payload["chain"] = chain
        _payload["payloadHash"] = payloadHash
        _headers = {"Content-type": "application/json"}

        _endpoint = self._CHAINWEB_ENDPOINT + f"/chain/{chain}/payload/{payloadHash}/outputs"
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        return r.json()

    def get_cut_network_peer_info(self, limit: int = None, next: str = None) -> dict:
        """Get cut-network peer info.

        Args:
            limit (int, optional): Maximum number of records that may be returned. The actual number may be lower. Defaults to None.
            next (str, optional): The cursor for the next page. This value can be found as value of the next property of the previous page. Defaults to None.

        Raises:
            TypeError: If limit or next is provided, then must be valid types.
            ValueError: If limit or next is provided, then must be valid values.
            HTTPError: If the request fails.

        Returns:
            dict: Cut-network peer info.
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

        _endpoint = self._CHAINWEB_ENDPOINT + "/cut/peer"
        _headers = {"Content-type": "application/json"}
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        return r.json()


    
    def get_chain_mempool_network_peer_info(self, chain: int, limit: int = None, next: str = None) -> dict:
        """__description__

        Args:
            chain (int): The id of the chain to which the request is sent
            limit (int, optional): Maximum number of records that may be returned. The actual number may be lower. Defaults to None.
            next (str, optional): The cursor for the next page. This value can be found as value of the next property of the previous page. Defaults to None.

        Raises:
            TypeError: if chain is not an integer or limit is not an integer or next is not a string
            ValueError: if chain is less than 0 or limit is less than 0
            HTTPError: if the request fails

        Returns:
            dict: __description__
        """                
        _payload = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(limit, int):
            raise TypeError("limit must be an integer")
        
        elif limit < 0:
            raise ValueError("limit must be greater than 0")
        
        if not isinstance(next, str):
            raise TypeError("next must be a string")

        _payload["chain"] = chain
        _payload["limit"] = limit
        _payload["next"] = next

        _endpoint = self._CHAINWEB_ENDPOINT + f"/chain/{chain}/mempool/peer"
        _headers = {"Content-type": "application/json"}
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        return r.json()

    def get_config(self) -> dict:
        """Get config of the Chainweb node.

        Raises:
            HTTPError: if the request fails.

        Returns:
            dict: Returns the configuration of chainweb-node as a JSON structure. Sensitive information is removed from the result. The JSON schema depends on the chainweb node version and is not part of the stable chainweb-node API.
        """                
        _endpoint = self._CHAINWEB_ENDPOINT + "/config"
        _headers = {"Content-type": "application/json"}
        r = requests.get(_endpoint, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        return r.json()
