from enum import Enum
import requests
from typing import Any, Dict, List, Optional, Tuple, Union
from kadenapy.url import GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint
import json
from typing import List

class MempoolEndpoints():
    """Mempool P2P endpoints for communication between mempools. Endusers are not supposed to use these endpoints directly. Instead, the respective Pact endpoints should be used for submitting transactions into the network.
    
    """
    def __init__(self, api: Union[GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint]):
        self.node = api

    
    def set_node_endpoint(self, api: Union[GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint]):
        """Set the node url that serves endpoints.

        Args:
            `api` (Union[GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint]): The node url that serves endpoints.
        """
        self.node = api


    def get_pending_transactions_from_the_mempool(self, chain:int, nonce:int = None, since:int = None):
        """Get pending transactions from the mempool.

        Args:
            `chain` (int): The id of the chain to which the request is sent.
            `nonce` (int, optional): Server nonce value. Defaults to None.
            `since` (int, optional): Mempool tx id value. Defaults to None.

        Raises:
            `TypeError`: If chain is not an integer.
            `ValueError`: If chain is less than 0. Also if nonce and since arguments are provided, they must be valid types.
            `Exception`: If the request fails.
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
        r = requests.post(_endpoint, params=_payload, headers=_headers)
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")
        return r.json()



    def check_for_pending_transactions_in_the_mempool(self, chain:int, requestKeys: List[str]):
        """Check for pending transactions in the mempool.

        Args:
            `chain` (int): The id of the chain to which the request is sent.
            `requestKeys` (List[str]): Array of strings (Base64Url Request key of a Pact transaction). 

        Raises:
            `TypeError`: If chain is not an integer or requestKeys is not a list.
            `ValueError`: If chain is less than 0.
            `Exception`: If the request fails.
        """                
        _payload = {}
        _data = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(requestKeys, list):
            raise TypeError("requestKeys must be a list of strings")
        
        _endpoint = self.node.endpoint + f"/chain/{chain}/mempool/member"
        _headers = {"Content-type": "application/json"}
        _data = requestKeys
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")
        
        return r.json()


    def lookup_pending_transactions_in_the_mempool(self, chain:int, requestKeys: list):
        """Lookup pending transactions in the mempool.

        Args:
            `chain` (int): The id of the chain to which the request is sent.
            `requestKeys` (List[str]): Array of strings (Base64Url Request key of a Pact transaction). 

        Raises:
            `TypeError`: If chain is not an integer or requestKeys is not a list.
            `ValueError`: If chain is less than 0 or requestKeys is not a list of valid base 64 url encoded strings.
            `Exception`: If the request fails.
        """                
        _payload = {}
        _data = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(requestKeys, list):
            raise TypeError("requestKeys must be a list of strings")
        
        _endpoint = self.node.endpoint + f"/chain/{chain}/mempool/lookup"
        _headers = {"Content-type": "application/json"}
        _data = requestKeys
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")
        
        return r.json()

    def insert_transactions_in_the_mempool(self, chain:int, signedTransactionTexts: List[str]):
        """Insert transactions into the mempool.

        Args:
            `chain` (int): The id of the chain to which the request is sent.
            `signedTransactionTexts` (List[str]): Array of strings (Text of a JSON encoded signed Pact transaction). 

        Raises:
            `TypeError`: If chain is not an integer or signedTransactions is not a list.
            `ValueError`: If chain is less than 0.
            `Exception`: If the request fails.

        Returns:
            dict: Pending transactions from the mempool.
        """                
        _payload = {}
        _data = {}
        if not isinstance(chain, int):
            raise TypeError("chain must be an integer")
        
        elif chain < 0:
            raise ValueError("chain must be greater than 0")
        
        if not isinstance(signedTransactionTexts, list):
            raise TypeError("signedTransactions must be a list of strings")
        
        _payload["chain"] = chain
        _endpoint = self.node.endpoint + f"/chain/{chain}/mempool/insert"

        _headers = {"Content-type": "application/json"}
        _data = signedTransactionTexts
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")
        
        return r.json()

    