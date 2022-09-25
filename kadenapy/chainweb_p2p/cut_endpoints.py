from enum import Enum
import requests
from typing import Any, Dict, List, Optional, Tuple, Union
from kadenapy.url import GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint
import json

class CutEndpoints():
    """A cut represents a distributed state of a chainweb. It references one block header for each chain, such that those blocks are pairwise concurrent.

Two blocks from two different chains are said to be concurrent if either one of them is an adjacent parent (is a direct dependency) of the other or if the blocks do not depend at all on each other.

    """
    def __init__(self, api: Union[GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint]):
        self.node = api

    
    def set_node_endpoint(self, api: Union[GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint]):
        """Set the node url that serves endpoints.

        Args:
            api (Union[GenericNodeAPIEndpoint, P2PBootstrapAPIEndpoint, ServiceAPIEndpoint]): The node url that serves endpoints.
        """
        self.node = api


    def get_current_cut(self, maxheight: int=None):
        """Query the current cut from a Chainweb node.

        Args:
            maxheight (int, optional): Maximum cut height of the returned cut. Defaults to None.

        Raises:
            TypeError: If maxheight is not an integer.
            ValueError: If maxheight is less than 0.
            Exception: If the request fails.
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
            raise Exception(f"Status {r.status_code}: {r.text}")
        return r.json()