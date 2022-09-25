from enum import Enum
import requests
from typing import Any, Dict, List, Optional, Tuple, Union
from kadenapy.url import GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint
import json
from typing import List

class BlockPayloadEndpoints():
    """Raw literal Block Payloads in the form in which they are stored on the chain. By default only the payload data is returned which is sufficient for validating the blockchain Merkle Tree. It is also sufficient as input to Pact for executing the Pact transactions of the block and recomputing the outputs.

It is also possible to query the transaction outputs along with the payload data.

    """
    def __init__(self, api: Union[GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint]):
        self.node = api

    
    def set_node_endpoint(self, api: Union[GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint]):
        """Set the node url that serves endpoints.

        Args:
            `api` (Union[GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint]): The node url that serves endpoints.
        """
        self.node = api


    def get_block_payload(self, chain: int, payloadHash: str):
        """Get block payload.

        Args:
            `chain` (int): The id of the chain to which the request is sent.
            `payloadHash` (str): Payload hash of a block.

        Raises:
            `TypeError`: If chain is not an integer or payloadHash is not a string.
            `ValueError`: If chain is less than 0 or payloadHash is not a valid base 64 url encoded string.
            `Exception`: If the request fails.
        """                
        _payload = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(payloadHash, str):
            raise TypeError("payloadHash must be an string")

        _headers = {"Content-type": "application/json"}
        _endpoint = self.node.endpoint + f"/chain/{chain}/payload/{payloadHash}"
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")
        
        return r.json()


    def get_batch_of_block_payload(self, chain:int, payloadHashes: list):
        """Get batch of block payloads.

        Args:
            `chain` (int): The id of the chain to which the request is sent.
            `payloadHashes` (list): A list of block payload hashes (Base64Url -without padding- encoded block payload hash).

        Raises:
            `TypeError`: If chain is not an integer or payloadHashes is not a list.
            `ValueError`: If chain is less than 0.
            `HTTPError`: If the request fails.
        """                
        _payload = {}
        _data = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(payloadHashes, list):
            raise TypeError("payloadHashes must be a list of strings")

        _endpoint = self.node.endpoint + f"/chain/{chain}/payload/batch"

        _headers = {"Content-type": "application/json"}
        _data['payloadHashes'] = payloadHashes
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")
        
        return r.json()

    def get_block_payload_with_outputs(self, chain: int, payloadHash: str) -> dict:
        """Get block payload with outputs.

        Args:
            `chain` (int): The id of the chain to which the request is sent.
            `payloadHash` (str): Payload hash of a block.

        Raises:
            `TypeError`: If chain is not an integer or payloadHash is not a string.
            `ValueError`: If chain is less than 0.
            `Exception`: If the request fails.
        """                
        _payload = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(payloadHash, str):
            raise TypeError("payloadHash must be an string")
        
        _payload["payloadHash"] = payloadHash
        _headers = {"Content-type": "application/json"}

        _endpoint = self.node.endpoint + f"/chain/{chain}/payload/{payloadHash}/outputs"
        r = requests.get(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")
        return r.json()

    def get_batch_of_block_payload_with_outputs(self, chain: int, payloadHashes: List[str]):
        """Get batch of block payloads with outputs.

        Args:
            `chain` (int): The id of the chain to which the request is sent.
            `payloadHashes` (List[str]): Array of strings (Base64Url -without padding- encoded block payload hash). 

        Raises:
            `TypeError`: If chain is not an integer or payloadHashes is not a list.
            `ValueError`: If chain is less than 0.
            `Exception`: If the request fails.
        """                
        _payload = {}
        _data = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(payloadHashes, list):
            raise TypeError("payloadHashes must be a list of strings")
        
        _endpoint = self.node.endpoint + f"/chain/{chain}/payload/outputs/batch"

        _headers = {"Content-type": "application/json"}
        _data['payloadHashes'] = payloadHashes
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        
        return r.json()
