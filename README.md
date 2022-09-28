# Kadena Chainweb Python Bindings

<div align="center">
  <img alt="Boards" width="50%" src="media/chainwebpy.png"/>
</div>


Chainweb.py is a high level Python bindings for the Kadena Chainweb REST API.


## Installation

```
pip3 install chainwebpy
```


## Quickstart

```
from chainwebpy.url import P2PBootstrapAPIEndpoint
from chainwebpy.chainweb_p2p.block_header_endpoints import BlockHeaderEndpoints

endpoint = P2PBootstrapAPIEndpoint(
    P2PBootstrapAPIEndpoint.TestnetNode.US1
)

cw = BlockHeaderEndpoints(endpoint)
block_headers = cw.get_block_headers(chain=0)
```

## How to Use


In order to call functions defined in endpoints, one must create an API endpoint object.

* `P2PBootstrapAPIEndpoint` is Chainweb P2P bootstrap node API endpoint. Used only for calling P2P API endpoints.


    ```
    from chainwebpy.url import P2PBootstrapAPIEndpoint
    endpoint = P2PBootstrapAPIEndpoint(
            P2PBootstrapAPIEndpoint.TestnetNode.US1
        )
    ```


* `ServiceAPIEndpoint` is Chainweb mainnet or testnet service API endpoint. Can be also used for some endpoints of the P2P API.


    ```
    from chainwebpy.url import ServiceAPIEndpoint
    endpoint = ServiceAPIEndpoint("testnet")
    ```

* `GenericNodeAPIEndpoint` is generic node API endpoint.

    ```
    from chainwebpy.url import GenericNodeAPIEndpoint
    endpoint = GenericNodeAPIEndpoint(
        scheme = "https",
        host = "us1.testnet.chainweb.com",
        port = 443,
        api_version = "0.0",
        chainweb_version = "0"
    )
    ```

After constructing `endpoint`, you can call bindings that is defined in `chainwebpy.chainweb_p2p` and `chainwebpy.chainweb_service`.

```
from chainwebpy.chainweb_p2p.cut_endpoints import CutEndpoints 
cw = CutEndpoints(endpoint)
```

## Implementation

The bindings implemenets high level functions for the following REST API endpoints:

- CHAINWEB P2P API
    - [X] Cut Endpoints
    - [X] Block Hashes Endpoints
    - [X] Block Header Endpoints
    - [X] Block Payload Endpoints
    - [X] Mempool P2P Endpoints
    - [X] Peer Endpoints
    - [X] Config Endpoints

- CHAINWEB SERVICE API
    - [X] Service API
    - [X] Miscellaneous Endpoints
    - [X] Mining Endpoints
    - [-] Pact Endpoints (To-Do)
    - [-] Rosetta Endpoints


## Structure

```
├── chainwebpy
    ├── __init__.py
    │
    ├── chainweb_p2p
    │   ├── block_hashes_endpoints.py
    │   ├── block_header_endpoints.py
    │   ├── block_payload_endpoints.py
    │   ├── config_endpoints.py
    │   ├── cut_endpoints.py
    │   ├── mempool_endpoints.py
    │   └── peer_endpoints.py
    │
    ├── chainweb_service
    │   ├── mining_endpoints.py
    │   ├── miscellaneous_endpoints.py
    │   └── pact_endpoints.py
    │
    └── url.py
```

## Endpoints

### Chainweb P2P


### BlockHashesEndpoints

```
from chainwebpy.chainweb_p2p.block_hashes_endpoints import BlockHashesEndpoints
```

These endpoints return block hashes from the chain database.

Generally, block hashes are returned in ascending order and include hashes from orphaned blocks.

For only querying blocks that are included in the winning branch of the chain the branch endpoint can be used, which returns blocks in descending order starting from the leafs of branches of the block chain.


### BlockHeaderEndpoints

```
from chainwebpy.chainweb_p2p.block_header_endpoints import BlockHeaderEndpoints
```

These endpoints return block headers from the chain database.

Generally, block headers are returned in ascending order and include headers of orphaned blocks.

For only querying blocks that are included in the winning branch of the chain the branch endpoints can be used, which return blocks in descending order starting from the leafs of branches of the block chain.


### BlockPayloadEndpoints
```
from chainwebpy.chainweb_p2p.block_payload_endpoints import BlockPayloadEndpoints
```

Raw literal Block Payloads in the form in which they are stored on the chain. By default only the payload data is returned which is sufficient for validating the blockchain Merkle Tree. It is also sufficient as input to Pact for executing the Pact transactions of the block and recomputing the outputs.

It is also possible to query the transaction outputs along with the payload data.


### ConfigEndpoints

```
from chainwebpy.chainweb_p2p.config_endpoints import ConfigEndpoints
```

### CutEndpoints
```
from chainwebpy.chainweb_p2p.cut_endpoints import CutEndpoints
```

A cut represents a distributed state of a chainweb. It references one block header for each chain, such that those blocks are pairwise concurrent.

Two blocks from two different chains are said to be concurrent if either one of them is an adjacent parent (is a direct dependency) of the other or if the blocks do not depend at all on each other.


### MempoolEndpoints
```
from chainwebpy.chainweb_p2p.mempool_endpoints import MempoolEndpoints
```
Mempool P2P endpoints for communication between mempools. Endusers are not supposed to use these endpoints directly. Instead, the respective Pact endpoints should be used for submitting transactions into the network.


### PeerEndpoints
```
from chainwebpy.chainweb_p2p.peer_endpoints import PeerEndpoints
```

## Chainweb Service

### Mining Endpoints
```
from chainwebpy.chainweb_service.mining_endpoints import MiningEndpoints
```

### MiscellaneousEndpoints
```
from chainwebpy.chainweb_service.miscellaneous_endpoints import MiscellaneousEndpoints
```

## Support and Help

* [Email](mailto:mert@yuugen.art)
* Discord: MertK#2634
* Telegram: mertkklu
* [Create an issue](https://github.com/justmert/chainweb.py/issues/new)