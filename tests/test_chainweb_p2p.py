from chainweb.chainweb_p2p import ChainwebP2P, TestnetNode, MainnetNode
import urllib.parse


def test_set_api_endpoint():
    p2p = ChainwebP2P()
    assert p2p.get_node_location == TestnetNode.US1
    assert p2p.get_api_endpoint == 'https://us1.testnet.chainweb.com/chainweb/0.0/testnet04'
    
    p2p.set_api_endpoint(node=MainnetNode.US_E1)
    assert p2p.get_node_location == MainnetNode.US_E1
    assert p2p.get_api_endpoint == 'https://us-e1.chainweb.com/chainweb/0.0/mainnet01'

    p2p.set_api_endpoint(node="https://tr1.chainweb.com/chainweb/0.0/mainnet02")
    assert p2p.get_api_endpoint == 'https://tr1.chainweb.com/chainweb/0.0/mainnet02'

    p2p.set_api_endpoint(api_version=0.1, node=TestnetNode.AP1)
    assert p2p.get_node_location == TestnetNode.AP1
    assert p2p.get_api_endpoint == 'https://ap1.testnet.chainweb.com/chainweb/0.1/testnet04'
    

def test_get_cut():
    p2p = ChainwebP2P()
    cut = p2p.get_cut()
    assert isinstance(cut, dict) and len(cut.keys()) > 0
    
    cut2 = p2p.get_cut(maxheight=12)
    assert cut2['height'] < 12


def test_get_block_hashes():
    p2p = ChainwebP2P()
    hashes = p2p.get_block_hashes(chain=1)
    assert isinstance(hashes, dict) and len(hashes.keys()) > 0
    
    hashes2 = p2p.get_block_hashes(chain=2)
    assert isinstance(hashes2, dict) and len(hashes2.keys()) > 0
    
    hashes3 = p2p.get_block_hashes(chain=2, limit= 10, next = hashes2['next'])
    assert isinstance(hashes3, dict) and len(hashes3.keys()) > 0
    
    hashes4 = p2p.get_block_hashes(chain=2, limit= 10, next = hashes3['next'], minheight=2, maxheight=4)
    assert isinstance(hashes4, dict) and len(hashes4.keys()) > 0
    

def test_get_block_headers():
    p2p = ChainwebP2P()
    headers = p2p.get_block_headers(chain=1)
    assert isinstance(headers, dict) and len(headers.keys()) > 0
    
    headers2 = p2p.get_block_headers(chain=2)
    assert isinstance(headers2, dict) and len(headers2.keys()) > 0
    
    headers3 = p2p.get_block_headers(chain=2, limit= 10, next = headers2['next'])
    assert isinstance(headers3, dict) and len(headers3.keys()) > 0
    
    headers4 = p2p.get_block_headers(chain=2, limit= 10, next = headers3['next'], minheight=2, maxheight=4)
    assert isinstance(headers4, dict) and len(headers4.keys()) > 0

    headers5 = p2p.get_block_headers(chain=2, limit= 10, next = headers3['next'], minheight=2, maxheight=4, responseSchema="base64url")
    print(headers5)
    print(type(headers5))