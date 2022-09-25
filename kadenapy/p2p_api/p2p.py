from enum import Enum
from urllib.error import HTTPError
import requests
import urllib.parse
import typing
from typing import Any, Dict, List, Optional, Tuple, Union
from kadenapy.url import GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint
import json

class ChainwebP2P():
    def __init__(self, api: Union[GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint]) -> None:
        """The P2P API is used for inter-node communication in order to establish block chain consensus. 
        Each chainweb-node serves these endpoints via HTTPS on a network interface and port that is available directly on the public internet.

        Additionally, endpoints of the P2P API can be made available for other clients. 
        For this purpose it is possible to expose the endpoints via reverse proxies, load balancers, or authentication frameworks, and similar web technologies.

        Args:
            api_version (int, optional): Chainweb API version. Defaults to "0.0".
            node (Union[TestnetNode, MainnetNode, str], optional): Node P2P bootstrap node that serves P2P API endpoints. Can be instance of TestnetNode or MainnetNode. Defaults to TestnetNode.US1.
            Also can be string of form "{schema}://{domain}:{port}/chainweb/{apiVersion}/{chainwebVersion}".
        """
        self.node = api

    def set_node_endpoint(self, api: Union[GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint]):
        """Set the node endpoint.

        Args:
            api_version (int, optional): Chainweb API version. Defaults to "0.0".
            node (Union[TestnetNode, MainnetNode, str], optional): Node P2P bootstrap node that serves P2P API endpoints. Can be instance of TestnetNode or MainnetNode. Defaults to TestnetNode.US1.
            Also can be string of form "{schema}://{domain}:{port}/chainweb/{apiVersion}/{chainwebVersion}".
        """
        self.node = api
        
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
        
        _endpoint = self.node.endpoint + "/cut"
        _headers = {"Content-type": "application/json"}
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
        _endpoint = self.node.endpoint + f"/chain/{chain}/hash"
        _headers = {"Content-type": "application/json"}
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        return r.json()
    
    def get_block_hash_branches(self, chain: int, lower:str, upper:str, limit: int = None, next: int = None, minHeight: int = None, maxHeight: int = None) -> dict:
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
        
        if not isinstance(lower, str):
            raise TypeError("lower must be a string")

        if not isinstance(upper, str):
            raise TypeError("upper must be a string")


        _payload["chain"] = chain
        _payload["lower"] = lower
        _payload["upper"] = upper
        _endpoint = self.node.endpoint + f"/chain/{chain}/hash/branch"

        _headers = {"Content-type": "application/json"}
        r = requests.post(_endpoint, params=_payload, headers=_headers)
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

        if responseSchema == "binary":
            _headers["Accept"] = "application/json"

        elif responseSchema == "object":
            _headers['Accept'] = "application/json;blockheader-encoding=object"

        _payload["chain"] = chain    
        _endpoint = self.node.endpoint + f"/chain/{chain}/header"
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        return r.json()

    def get_block_headers_by_hash(self, chain: int, blockHash: str, responseSchema: str = "object") -> Union[dict, bytes, str]: # GET METHOD
        """Query a block header by its hash.

        Args:
            chain (int): The id of the chain to which the request is sent.
            blockHash (str): Block hash of a block.
            responseScheme (str, optional): Response scheme. Can be one of "object", "base64url", or "binary". Defaults to "object".

        Raises:
            TypeError: If chain is not an integer or blockHash is not a string.
            ValueError: If chain is less than 0.
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
        
        if responseSchema not in ["object", "base64url", "binary"]:
            raise ValueError("responseScheme must be one of 'object', 'base64url', or 'binary'")

        
        _headers = {"Content-type": "application/json"}

        if responseSchema == "object":
            _headers['Accept'] = "application/json;blockheader-encoding=object"

        elif responseSchema == "base64url":
            _headers['Accept'] = "application/json"

        elif responseSchema == "binary":
            _headers['Accept'] = "application/octet-stream"

        _payload["chain"] = chain
        _payload["blockHash"] = blockHash
        _endpoint = self.node.endpoint + f"/chain/{chain}/header/{blockHash}"
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code == 404:
            raise Exception(f"Key not found.")
        elif r.status_code != 200:
            raise Exception(f"Status Code: {r.status_code}")
        
        if responseSchema == "binary":
            return r.content
        return r.json()

    def get_block_header_branches(self, chain:int, lower:list, upper:list, limit: int = None, next: str = None, minHeight: int = None, maxHeight: int = None):
        """Query a block header by its hash.

        Args:
            chain (int): The id of the chain to which the request is sent.
            lower (str): Block hash of a block.
            upper (str): Block hash of a block.
            limit (int, optional): Maximum number of records that may be returned. The actual number may be lower. Defaults to None.
            next (str, optional): The cursor for the next page. This value can be found as value of the next property of the previous page. Defaults to None.
            minHeight (int, optional): Minimum block height of the returned headers. Defaults to None.
            maxHeight (int, optional): Maximum block height of the returned headers. Defaults to None.

        Raises:
            TypeError: If chain is not an integer or blockHash is not a string.
            ValueError: If chain is less than 0.
            HTTPError: If the request fails.

        Returns:
            str: Base64Url (without padding) encoded binary block header
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

        _payload["chain"] = chain
        _endpoint = self.node.endpoint + f"/chain/{chain}/header/branch"

        _headers = {"Content-type": "application/json"}
        _data['lower'] = lower
        _data['upper'] = upper
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"{r.status_code} {r.text}")
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
        
        # elif not p2p_utils._isBase64(payloadHash):
        #     raise ValueError("payloadHash must be a valid base 64 string")

        _payload["chain"] = chain
        _payload["payloadHash"] = payloadHash

        _headers = {"Content-type": "application/json"}
        _endpoint = self.node.endpoint + f"/chain/{chain}/payload/{payloadHash}"
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code == 404:
            raise Exception(f"Key not found.")

        elif r.status_code != 200:
            raise Exception(f"{r.status_code}")
        
        return r.json()

    def get_batch_of_block_payload(self, chain:int, payloadHashes: list):
        """Get batch of block payloads.

        Args:
            chain (int): The id of the chain to which the request is sent.
            payloadHashes (list): List of payload hashes of blocks.

        Raises:
            TypeError: If chain is not an integer or payloadHashes is not a list.
            ValueError: If chain is less than 0 or payloadHashes is not a list of valid base 64 url encoded strings.
            HTTPError: If the request fails.

        Returns:
            dict: Block payloads.
        """                
        _payload = {}
        _data = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(payloadHashes, list):
            raise TypeError("payloadHashes must be a list of strings")
        
        # elif not p2p_utils._isBase64(payloadHash):
        #     raise ValueError("payloadHash must be a valid base 64 string")

        _payload["chain"] = chain
        _endpoint = self.node.endpoint + f"/chain/{chain}/payload/batch"

        _headers = {"Content-type": "application/json"}
        _data['payloadHashes'] = payloadHashes
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code == 404:
            raise Exception(f"Key not found.")

        elif r.status_code != 200:
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
        
        # elif not p2p_utils._isBase64(payloadHash):
        #     raise ValueError("payloadHash must be a valid base 64 string")

        _payload["chain"] = chain
        _payload["payloadHash"] = payloadHash
        _headers = {"Content-type": "application/json"}

        _endpoint = self.node.endpoint + f"/chain/{chain}/payload/{payloadHash}/outputs"
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        return r.json()

    def get_batch_of_block_payload_with_outputs(self, chain: int, payloadHashes: list):
        """Get batch of block payloads with outputs.

        Args:
            chain (int): The id of the chain to which the request is sent.
            payloadHashes (list): List of payload hashes of blocks.

        Raises:
            TypeError: If chain is not an integer or payloadHashes is not a list.
            ValueError: If chain is less than 0 or payloadHashes is not a list of valid base 64 url encoded strings.
            HTTPError: If the request fails.

        Returns:
            dict: Block payloads with outputs.
        """                
        _payload = {}
        _data = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(payloadHashes, list):
            raise TypeError("payloadHashes must be a list of strings")
        
        # elif not p2p_utils._isBase64(payloadHash):
        #     raise ValueError("payloadHash must be a valid base 64 string")

        _payload["chain"] = chain
        _endpoint = self.node.endpoint + f"/chain/{chain}/payload/outputs"

        _headers = {"Content-type": "application/json"}
        _data['payloadHashes'] = payloadHashes
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        
        return r.json()

    def get_pending_transactions_from_the_mempool(self, chain:int, nonce:int = None, since:int = None):
        """Get pending transactions from the mempool.

        Args:
            chain (int): The id of the chain to which the request is sent.
            nonce (int, optional): The nonce of the transaction. Defaults to None.
            since (int, optional): The timestamp of the transaction. Defaults to None.

        Raises:
            TypeError: If chain is not an integer or nonce is not an integer or since is not an integer.
            ValueError: If chain is less than 0 or nonce is less than 0 or since is less than 0.
            HTTPError: If the request fails.

        Returns:
            dict: Pending transactions from the mempool.
        """                
        _payload = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if nonce is not None:
            if not isinstance(nonce, int):
                raise TypeError("nonce must be an integer")
            
            elif nonce < 0:
                raise ValueError("nonce must be greater than 0")
            
            _payload["nonce"] = nonce
        
        if since is not None:
            if not isinstance(since, int):
                raise TypeError("since must be an integer")
            
            elif since < 0:
                raise ValueError("since must be greater than 0")
            
            _payload["since"] = since

        _headers = {"Content-type": "application/json"}
        _endpoint = self.node.endpoint + f"/chain/{chain}/mempool/getPending"
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        return r.json()

    def check_for_pending_transactions_in_the_mempool(self, chain:int, requestKeys: list):
        """Check for pending transactions in the mempool.

        Args:
            chain (int): The id of the chain to which the request is sent.
            requestKeys (list): List of transaction keys.

        Raises:
            TypeError: If chain is not an integer or requestKeys is not a list.
            ValueError: If chain is less than 0 or requestKeys is not a list of valid base 64 url encoded strings.
            HTTPError: If the request fails.

        Returns:
            dict: Pending transactions from the mempool.
        """                
        _payload = {}
        _data = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(requestKeys, list):
            raise TypeError("requestKeys must be a list of strings")
        
        _payload["chain"] = chain
        _endpoint = self.node.endpoint + f"/chain/{chain}/mempool/member"

        _headers = {"Content-type": "application/json"}
        _data['requestKeys'] = requestKeys
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        
        return r.json()

    def lookup_pending_transactions_in_the_mempool(self, chain:int, requestKeys: list):
        """Lookup pending transactions in the mempool.

        Args:
            chain (int): The id of the chain to which the request is sent.
            requestKeys (list): List of transaction keys.

        Raises:
            TypeError: If chain is not an integer or requestKeys is not a list.
            ValueError: If chain is less than 0 or requestKeys is not a list of valid base 64 url encoded strings.
            HTTPError: If the request fails.

        Returns:
            dict: Pending transactions from the mempool.
        """                
        _payload = {}
        _data = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(requestKeys, list):
            raise TypeError("requestKeys must be a list of strings")
        
        _payload["chain"] = chain
        _endpoint = self.node.endpoint + f"/chain/{chain}/mempool/lookup"

        _headers = {"Content-type": "application/json"}
        _data['requestKeys'] = requestKeys
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        
        return r.json()

    def insert_transactions_in_the_mempool(self, chain:int, signedTransactions: list):
        """Insert transactions in the mempool.

        Args:
            chain (int): The id of the chain to which the request is sent.
            signedTransactions (list): List of signed transactions.

        Raises:
            TypeError: If chain is not an integer or signedTransactions is not a list.
            ValueError: If chain is less than 0 or signedTransactions is not a list of valid base 64 url encoded strings.
            HTTPError: If the request fails.

        Returns:
            dict: Pending transactions from the mempool.
        """                
        _payload = {}
        _data = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(signedTransactions, list):
            raise TypeError("signedTransactions must be a list of strings")
        
        _payload["chain"] = chain
        _endpoint = self.node.endpoint + f"/chain/{chain}/mempool/insert"

        _headers = {"Content-type": "application/json"}
        _data['signedTransactions'] = signedTransactions
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
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

        _endpoint = self.node.endpoint + "/cut/peer"
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

        _payload["chain"] = chain

        _endpoint = self.node.endpoint + f"/chain/{chain}/mempool/peer"
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
        _endpoint = self.node.endpoint + "/config"
        _headers = {"Content-type": "application/json"}
        r = requests.get(_endpoint, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        return r.json()
