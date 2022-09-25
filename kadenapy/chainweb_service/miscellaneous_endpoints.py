import requests
from typing import Union
from kadenapy.url import (
    GenericNodeAPIEndpoint,
    P2PBootstrapAPIEndpoint,
    ServiceAPIEndpoint,
)
import json


class MiscellaneousEndpoints:
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

    def start_a_backup_job(self, backupPact=None):
        _payload = {}
        _data = {}
        _endpoint = self.node.endpoint + "/make-backup"

        _payload["backupPact"] = backupPact
        _headers = {"Content-type": "application/json"}
        r = requests.post(
            _endpoint, params=_payload, headers=_headers, data=json.dumps(_data)
        )
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")

        return r.json()

    def check_the_status_of_a_backup_job(self, backupId: str):
        """Check the status of a backup job.

        Args:
            backupId (str): The identifier of the backup being checked

        Raises:
            Exception: If the request fails.
        """
        _payload = {}
        _data = {}
        if backupId is None:
            raise Exception("backupId is required")

        if not isinstance(backupId, str):
            raise Exception("backupId must be a string")

        _endpoint = self.node.endpoint + f"/check-backup/{backupId}"

        _headers = {"Content-type": "application/json"}
        r = requests.get(
            _endpoint, params=_payload, headers=_headers, data=json.dumps(_data)
        )
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")

        return r.json()

    def health_check(self):
        """Checks whether the chainweb-node is up and running and responding to API requests. In order to check the state of consensus the /cut/get endpoint should be used instead.

        Raises:
            Exception: If the request fails.
        """
        _payload = {}
        _data = {}
        _endpoint = self.node.endpoint + "/health-check"

        _headers = {"Content-type": "application/json"}
        r = requests.get(
            _endpoint, params=_payload, headers=_headers, data=json.dumps(_data)
        )
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")

        return r.json()

    def general_node_info(self):
        """Provides general information about the node and the chainweb version

        Raises:
            Exception: If the request fails.
        """
        _payload = {}
        _data = {}
        _endpoint = self.node.endpoint + "/info"

        _headers = {"Content-type": "application/json"}
        r = requests.get(
            _endpoint, params=_payload, headers=_headers, data=json.dumps(_data)
        )
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")

        return r.json()

    def blocks_event_stream(self):
        """An source of server events that emits a BlockHeader event for each new block header that is added to the chain database of the remote node.

        The stream contains blocks that may later become orphaned. It is therefor recommended to buffer events on the client side for the most recent block heights until the desired confirmation depth is reached.

        The server may terminate this stream from time to time and it is up to the client to reinitiate the stream.

                Raises:
                    Exception: If the request fails.
        """
        _payload = {}
        _data = {}
        _endpoint = self.node.endpoint + "/header/updates"

        _headers = {"Content-type": "application/json"}
        r = requests.get(
            _endpoint, params=_payload, headers=_headers, data=json.dumps(_data)
        )
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}: {r.text}")

        return r.json()
