import urllib.parse
from unittest import TestCase
import pytest
from kadenapy.url import P2PBootstrapAPIEndpoint
from kadenapy.chainweb_p2p.block_hashes_endpoints import BlockHashesEndpoints

# def test_set_api_endpoint():

#     p2p = ChainwebP2P()
#     assert p2p.get_node_location == TestnetNode.US1
#     assert p2p.get_api_endpoint == 'https://us1.testnet.chainweb.com/chainweb/0.0/testnet04'
    
#     p2p.set_api_endpoint(node=MainnetNode.US_E1)
#     assert p2p.get_node_location == MainnetNode.US_E1
#     assert p2p.get_api_endpoint == 'https://us-e1.chainweb.com/chainweb/0.0/mainnet01'

#     p2p.set_api_endpoint(node="https://tr1.chainweb.com/chainweb/0.0/mainnet02")
#     assert p2p.get_api_endpoint == 'https://tr1.chainweb.com/chainweb/0.0/mainnet02'

#     p2p.set_api_endpoint(api_version=0.1, node=TestnetNode.AP1)
#     assert p2p.get_node_location == TestnetNode.AP1
#     assert p2p.get_api_endpoint == 'https://ap1.testnet.chainweb.com/chainweb/0.1/testnet04'
    

# def test_get_cut():
#     p2p = ChainwebP2P()
#     cut = p2p.get_cut()
#     assert isinstance(cut, dict) and len(cut.keys()) > 0
    
#     cut2 = p2p.get_cut(maxheight=12)
#     assert cut2['height'] < 12


# def test_get_block_hashes():
#     p2p = ChainwebP2P()
#     hashes = p2p.get_block_hashes(chain=1)
#     assert isinstance(hashes, dict) and len(hashes.keys()) > 0
    
#     hashes2 = p2p.get_block_hashes(chain=2)
#     assert isinstance(hashes2, dict) and len(hashes2.keys()) > 0
    
#     hashes3 = p2p.get_block_hashes(chain=2, limit= 10, next = hashes2['next'])
#     assert isinstance(hashes3, dict) and len(hashes3.keys()) > 0
    
#     hashes4 = p2p.get_block_hashes(chain=2, limit= 10, next = hashes3['next'], minheight=2, maxheight=4)
#     assert isinstance(hashes4, dict) and len(hashes4.keys()) > 0
    

# def test_get_block_headers():
#     p2p = ChainwebP2P()
#     headers = p2p.get_block_headers(chain=1)
#     assert isinstance(headers, dict) and len(headers.keys()) > 0
    
#     headers2 = p2p.get_block_headers(chain=2)
#     assert isinstance(headers2, dict) and len(headers2.keys()) > 0
    
#     headers3 = p2p.get_block_headers(chain=2, limit= 10, next = headers2['next'])
#     assert isinstance(headers3, dict) and len(headers3.keys()) > 0
    
#     headers4 = p2p.get_block_headers(chain=2, limit= 10, minheight=2, maxheight=241)
#     assert isinstance(headers4, dict) and len(headers4.keys()) > 0

#     headers5 = p2p.get_block_headers(chain=2, limit=2, responseSchema="base64url")
#     assert isinstance(headers5, dict) and len(headers5.keys()) > 0

#     headers6 = p2p.get_block_headers(chain=2, limit=2, responseSchema="object")
#     assert isinstance(headers6, dict) and len(headers6.keys()) > 0

#     with pytest.raises(ValueError):
#         p2p.get_block_headers(chain=2, limit=2, responseSchema="???")
    
#     with pytest.raises(ValueError):
#         p2p.get_block_headers(chain=-1, limit=2)
        
#     with pytest.raises(TypeError):
#         p2p.get_block_headers(chain=2, limit="dwad")

#     with pytest.raises(TypeError):
#         p2p.get_block_headers(chain=2, minheight="ada")
    
#     with pytest.raises(TypeError):
#         p2p.get_block_headers(chain=2, maxheight="ew")
    
#     assert isinstance(headers5, dict) and len(headers5.keys()) > 0

# def test_get_block_headers_by_hash():
#     p2p = ChainwebP2P()
#     hash = "5srZ_cRjnVIMNPdLU-HN0_G4hXrfh9wZ0tWjS0Rp3Sk"
#     wrong_hash = "5srZ_cRjnVIMNPdLU-HN0_G4hXrfh9wZ0tWjS0Rp3Sw"
#     a = p2p.get_block_headers_by_hash(chain=1, blockHash=hash, responseSchema="object")
#     assert isinstance(a, dict) and len(a.keys()) > 0

#     b = p2p.get_block_headers_by_hash(chain=1, blockHash=hash, responseSchema="binary")
#     assert isinstance(a, bytes)

#     c = p2p.get_block_headers_by_hash(chain=1, blockHash=hash, responseSchema="base64url")
#     assert isinstance(c, str) and len(c) > 0

#     with pytest.raises(Exception):
#         p2p.get_block_headers_by_hash(chain=1, blockHash=wrong_hash, responseSchema="object")


# def test_get_block_payload():
#     p2p = ChainwebP2P()
#     hash = "Y-muSAFQHd4L3Mkb9FIrM65oDCosd4dg35qPVUJhtEU"
#     wrong_hash = "Y-muSAFQHd4L3Mkb9FIrM65oDCosd4dg35qPVUJhtEP"

#     p2p.get_block_payload(chain=1, payloadHash=hash)
    
#     with pytest.raises(Exception):
#         p2p.get_block_payload(chain=1, payloadHash=wrong_hash)

# def test_get_payload_with_outputs():
#     p2p = ChainwebP2P()
#     hash = "Y-muSAFQHd4L3Mkb9FIrM65oDCosd4dg35qPVUJhtEU"
#     wrong_hash = "Y-muSAFQHd4L3Mkb9FIrM65oDCosd4dg35qPVUJhtEP"

#     a = p2p.get_payload_with_outputs(chain=1, payloadHash=hash)
#     assert isinstance(a, dict) and len(a.keys()) > 0

#     with pytest.raises(Exception):
#         p2p.get_payload_with_outputs(chain=1, payloadHash=wrong_hash)

# def test_get_cut_network_peer_info():
#     p2p = ChainwebP2P()
#     a = p2p.get_cut_network_peer_info()
#     assert isinstance(a, dict) and len(a.keys()) > 0
    
#     b = p2p.get_cut_network_peer_info(limit = 10)
#     assert b['limit'] <= 10

#     c = p2p.get_cut_network_peer_info(limit = 2)
#     assert c['limit'] <= 2

# def test_get_chain_mempool_network_peer_info():
#     p2p = ChainwebP2P()
#     a = p2p.get_chain_mempool_network_peer_info(chain=1)
#     assert isinstance(a, dict) and len(a.keys()) > 0
    
#     b = p2p.get_chain_mempool_network_peer_info(chain=1, limit = 10)
#     assert b['limit'] <= 10

#     c = p2p.get_chain_mempool_network_peer_info(chain=1, limit = 2)
#     assert c['limit'] <= 2

# def test_get_config():
#     p2p = ChainwebP2P()
#     a = p2p.get_config()
#     assert isinstance(a, dict) and len(a.keys()) > 0


def test_get_block_hash_branches():
    from kadenapy.url import P2PBootstrapAPIEndpoint
    from kadenapy.p2p_api.p2p import ChainwebP2P

    p2p_endpoint = P2PBootstrapAPIEndpoint(P2PBootstrapAPIEndpoint.MainnetNode.US_E1)
    
    p2p = ChainwebP2P(p2p_endpoint)

    a = p2p.get_batch_of_block_payload(chain=1, payloadHashes= ["svBDJwcgAqEOyZdXyA-Tl4fN_IGA4LOImGQd_NknK0Q"])
    print(a)



    assert isinstance(a, dict) and len(a.keys()) > 0