from enum import Enum
import requests
from typing import Any, Dict, List, Optional, Tuple, Union
from kadenapy.url import GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint
import json
from typing import List

class MiscellaneousEndpoints():
    """The Mining API of Chainweb node is disabled by default. It can be enabled and configured in the configuration file.

The mining API consists of the following endpoints that are described in detail on the Chainweb mining wiki page.
    """
    def __init__(self, api: Union[GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint]):
        self.node = api

    
    def set_node_endpoint(self, api: Union[GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint]):
        """Set the node url that serves endpoints.

        Args:
            `api` (Union[GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint]): The node url that serves endpoints.
        """
        self.node = api

    def get_mining_work(self, account:str, publicKeys: List[str], predicate: str = "keys-all"):
        """Get mining work.

        Args:
            `account` (str): The account name.
            `publicKeys` (List[str]): List of Miner public keys.
            `predicate` (str, optional): The predicate. Can be either "keys-all" or "keys-any". Defaults to "keys-all". 

        Raises:
            `TypeError`: If account is not a string or publicKeys is not a list or predicate is not a string.
            `Exception`: If the request fails.

        Returns:
            dict: Mining work.
        """                
        _payload = {}
        _data = {}
        if not isinstance(account, str):
            raise TypeError("account must be a string")
                
        if not isinstance(publicKeys, list):
            raise TypeError("publicKeys must be a list of strings")
        
        if not isinstance(predicate, str):
            raise TypeError("predicate must be a string")
        
        elif predicate not in ["keys-all", "keys-any"]:
            raise ValueError("predicate must be either keys-all or keys-any")
        
        _endpoint = self.node.endpoint + f"/mining/work/{account}"
        _headers = {"Content-type": "application/json"}
        _data["account"] = account
        _data['predicate'] = predicate
        _data['public-keys'] = publicKeys
        r = requests.get(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")
        
        return r.json()


    def solved_mining_work(self, workHeaderBytes: bytes):
        """Solved mining work.

        Args:
            `workHeaderBytes` (bytes): The solved PoW work header bytes
            byte (286 Solved PoW Work Header Bytes)
            The original work received that was received from /mining/work with updated nonce value such that it satisfies the Proof-of-Work. The nonce are last 8 bytes of the work header bytes.

            The PoW hash of a valid block is computed using blake2s. It must not be larger than the PoW target for the current block. The target was received along with the work header bytes from the /mining/work endpoint. For arithmetic comparisons the hash-target and the PoW hash are interpreted as unsigned 256 bit integral number in little endian encoding.

            Miners are free but not required to also update the creation time. The value must be strictly larger than the creation time of the parent block and must not be in the future.

        Raises:
            `TypeError`: If workHeaderBytes is not bytes.
            `Exception`: If the request fails.
        """                
        _payload = {}
        if not isinstance(workHeaderBytes, bytes):
            raise TypeError("workHeaderBytes must be bytes")
        
        _endpoint = self.node.endpoint + "/mining/solved"
        _headers = {"Content-type": "application/octet-stream"}
        _data = workHeaderBytes
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")
        
        return r.json()

