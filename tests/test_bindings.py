# flake8: noqa
import urllib.parse
from unittest import TestCase
import pytest
from chainwebpy.url import P2PBootstrapAPIEndpoint
from chainwebpy.chainweb_p2p.block_hashes_endpoints import BlockHashesEndpoints


def test_block_hashes_endpoints():
    from chainwebpy.url import P2PBootstrapAPIEndpoint
    from chainwebpy.chainweb_p2p.block_hashes_endpoints import (
        BlockHashesEndpoints,
    )

    p2p_endpoint = P2PBootstrapAPIEndpoint(
        P2PBootstrapAPIEndpoint.TestnetNode.US1
    )

    cw = BlockHashesEndpoints(p2p_endpoint)
    r1 = cw.get_block_hashes(0, limit=1)
    assert isinstance(r1, dict) and r1 is not None

    r2 = cw.get_block_hashes(
        0, limit=10, next=r1["next"], minheight=0, maxheight=100
    )
    assert isinstance(r2, dict) and r2 is not None

    cw.set_node_endpoint(
        P2PBootstrapAPIEndpoint(P2PBootstrapAPIEndpoint.TestnetNode.US1)
    )
    r3 = cw.get_block_hash_branches(
        0, lower=[r2["items"][0]], upper=[r2["items"][-1]]
    )
    assert isinstance(r3, dict) and r3 is not None


def test_block_header_endpoints():
    from chainwebpy.chainweb_p2p.block_header_endpoints import (
        BlockHeaderEndpoints,
    )

    p2p_endpoint = P2PBootstrapAPIEndpoint(
        P2PBootstrapAPIEndpoint.TestnetNode.US1
    )

    cw = BlockHeaderEndpoints(p2p_endpoint)
    r1 = cw.get_block_headers(0)
    assert isinstance(r1, dict) and r1 is not None

    r2 = cw.get_block_headers(0, limit=10, minheight=0, maxheight=100)
    assert isinstance(r2, dict) and r2 is not None
    example_hash = "_9LGDllHdcB_ZLyZMQvPTEuWOBCdJ1FnegysqbF31HQ"
    r3 = cw.get_block_headers_by_hash(0, blockHash=example_hash)
    assert isinstance(r3, dict) and r3 is not None

    r4 = cw.get_block_headers_by_hash(
        0, blockHash=example_hash, responseSchema="base64url"
    )
    assert r4 is not None

    r4 = cw.get_block_headers_by_hash(0, blockHash=example_hash)
    assert r4 is not None


def test_block_payload_endpoints():
    from chainwebpy.url import P2PBootstrapAPIEndpoint
    from chainwebpy.chainweb_p2p.block_payload_endpoints import (
        BlockPayloadEndpoints,
    )

    p2p_endpoint = P2PBootstrapAPIEndpoint(
        P2PBootstrapAPIEndpoint.TestnetNode.US1
    )

    example_hash = "WDeeKn0XomfXe94EK03AalihS8fW2jyyT6TeA2q75B4"
    cw = BlockPayloadEndpoints(p2p_endpoint)
    r1 = cw.get_block_payload(0, payloadHash=example_hash)
    assert isinstance(r1, dict) and r1 is not None

    r2 = cw.get_block_payload(0, payloadHash=example_hash)
    assert isinstance(r2, dict) and r2 is not None

    r3 = cw.get_block_payload_with_outputs(0, payloadHash=example_hash)
    assert isinstance(r3, dict) and r3 is not None

    r4 = cw.get_batch_of_block_payload(0, payloadHashes=[example_hash])
    assert r4 is not None

    r5 = cw.get_batch_of_block_payload_with_outputs(
        0, payloadHashes=[example_hash]
    )
    assert r5 is not None


def test_cut_endpoints():
    from chainwebpy.url import P2PBootstrapAPIEndpoint
    from chainwebpy.chainweb_p2p.cut_endpoints import CutEndpoints

    p2p_endpoint = P2PBootstrapAPIEndpoint(
        P2PBootstrapAPIEndpoint.TestnetNode.US1
    )

    cw = CutEndpoints(p2p_endpoint)

    r1 = cw.get_current_cut()
    assert isinstance(r1, dict) and r1 is not None

    r2 = cw.get_current_cut(maxheight=120)
    assert isinstance(r2, dict) and r2 is not None


def test_mempool_p2p_endpoints():
    from chainwebpy.url import P2PBootstrapAPIEndpoint
    from chainwebpy.chainweb_p2p.mempool_endpoints import MempoolEndpoints

    p2p_endpoint = P2PBootstrapAPIEndpoint(
        P2PBootstrapAPIEndpoint.TestnetNode.US1
    )

    cw = MempoolEndpoints(p2p_endpoint)

    r1 = cw.get_pending_transactions_from_the_mempool(chain=1)
    assert isinstance(r1, dict) and r1 is not None

    r2 = cw.check_for_pending_transactions_in_the_mempool(
        chain=1, requestKeys=["MLOST-liM4bLiuBtrjK5L9-4GynKUejcnp-cgKKlxzU"]
    )
    assert r2 is not None

    r3 = cw.lookup_pending_transactions_in_the_mempool(
        chain=1, requestKeys=["MLOST-liM4bLiuBtrjK5L9-4GynKUejcnp-cgKKlxzU"]
    )
    assert r3 is not None


def test_peer_endpoints():
    from chainwebpy.url import P2PBootstrapAPIEndpoint
    from chainwebpy.chainweb_p2p.peer_endpoints import PeerEndpoints

    p2p_endpoint = P2PBootstrapAPIEndpoint(
        P2PBootstrapAPIEndpoint.TestnetNode.US1
    )

    cw = PeerEndpoints(p2p_endpoint)

    r1 = cw.get_cut_network_peer_info()
    assert isinstance(r1, dict) and r1 is not None

    r2 = cw.get_chain_mempool_network_peer_info(chain=1)
    assert isinstance(r2, dict) and r2 is not None
