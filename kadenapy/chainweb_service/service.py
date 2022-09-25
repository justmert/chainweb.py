from typing import Any, Dict, List, Optional, Tuple, Union
from kadenapy.url import GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint
import requests
import json

class ChainwebService():
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

    
    def start_a_backup_job(self, backupPact = None):      
        _payload = {}
        _data = {}
        _endpoint = self.node.endpoint + f"/make-backup"

        _headers = {"Content-type": "application/json"}
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        
        return r.json()

    def check_the_status_of_a_backup_job(self, backupId:str):
        _payload = {}
        _data = {}
        if backupId is None:
            raise Exception("backupId is required")

        if not isinstance(backupId, str):
            raise Exception("backupId must be a string")

        _endpoint = self.node.endpoint + f"/check-backup/{backupId}"

        _headers = {"Content-type": "application/json"}
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        
        return r.json()

    def health_check(self):
        _payload = {}
        _data = {}
        _endpoint = self.node.endpoint + f"/health-check"

        _headers = {"Content-type": "application/json"}
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        
        return r.json()

    def general_node_info(self):
        _payload = {}
        _data = {}
        _endpoint = self.node.endpoint + f"/info"

        _headers = {"Content-type": "application/json"}
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        
        return r.json()

    def blocks_event_stream(self):
        _payload = {}
        _data = {}
        _endpoint = self.node.endpoint + f"/header/updates"

        _headers = {"Content-type": "application/json"}
        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        
        return r.json()

    
    def get_mining_work(self, account:str, predicate: str, publicKeys: list):
        _payload = {}
        _data = {}
        if account is None:
            raise Exception("account is required")

        if not isinstance(account, str):
            raise Exception("account must be a string")

        if predicate is None:
            raise Exception("predicate is required")

        if not isinstance(predicate, str):
            raise Exception("predicate must be a string")

        if publicKeys is None:
            raise Exception("publicKeys is required")

        if not isinstance(publicKeys, list):
            raise Exception("publicKeys must be a list")

        _endpoint = self.node.endpoint + f"/mining/work/{account}/{predicate}"

        _headers = {"Content-type": "application/json"}
        _data = {"account": account,
                "predicate": predicate,
                "public-keys": publicKeys}

        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        
        return r.json()

    def solved_mining_work(self, solvedWorkHeaderByte: bytes):
        _payload = {}
        _data = {}
        if solvedWorkHeaderByte is None:
            raise Exception("solvedWorkHeaderByte is required")

        if not isinstance(solvedWorkHeaderByte, bytes):
            raise Exception("solvedWorkHeaderByte must be a bytes")

        _endpoint = self.node.endpoint + f"/mining/solved"

        _headers = {"Content-type": "application/octet-stream"}
        _data = solvedWorkHeaderByte

        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        
        return r.json()

    def notification_of_updated_work(self, chainIDBytes: bytes):
        _payload = {}
        _data = {}
        if chainIDBytes is None:
            raise Exception("chainIDBytes is required")

        if not isinstance(chainIDBytes, bytes):
            raise Exception("chainIDBytes must be a bytes")

        _endpoint = self.node.endpoint + f"/mining/updated"

        _headers = {"Content-type": "application/octet-stream"}
        _data = chainIDBytes

        r = requests.post(_endpoint, params=_payload, headers=_headers, data=json.dumps(_data))
        if r.status_code != 200:
            raise Exception(f"{r.status_code}")
        
        return r.json()

    