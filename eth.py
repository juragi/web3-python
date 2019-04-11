from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
from web3.auto import w3
import sys, json, requests
from hexbytes import HexBytes

class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)

web3 = Web3(HTTPProvider('https://mainnet.infura.io/v3/d7c9200d82e444f3a8f1871fb30b9467'))
command = sys.argv[1]

#python3.6 eth.py balance address
if command == 'balance':
    address = sys.argv[2]
    print(web3.fromWei(web3.eth.getBalance(Web3.toChecksumAddress(address)), 'ether'))

#python3.6 eth.py send fromAddress ethAmount toAddress privateKey
elif command == 'send':
    fromAddress = sys.argv[2]
    amount = web3.toWei(float(sys.argv[3]), 'ether')
    toAddress = sys.argv[4]
    priv = sys.argv[5]
    signed_txn = web3.eth.account.signTransaction(dict(
        nonce=web3.eth.getTransactionCount(Web3.toChecksumAddress(fromAddress)),
        gasPrice=web3.eth.gasPrice,
        gas=100000,
        to=Web3.toChecksumAddress(toAddress),
        value=amount
        ),priv
    )
    print(web3.eth.sendRawTransaction(signed_txn.rawTransaction).hex())

#python3.6 eth.py create
elif command == 'create':
    r = requests.post(url='https://api.blockcypher.com/v1/eth/main/addrs')
    d = json.loads(r.text)
    print('0x' + d['address'] + ',' + d['private'])

#python3.6 eth.py last
elif command == 'last':
    print(web3.eth.getBlock('latest')['number'])

#python3.6 eth.py block blockNumber
elif command == 'block':
    blockNumber = int(sys.argv[2])
    d = web3.eth.getBlock(blockNumber).__dict__
    print(json.dumps(d, cls=HexJsonEncoder))

#python3.6 eth.py tx txid
elif command == 'tx':
    txid = sys.argv[2]
    d = web3.eth.getTransaction(txid).__dict__
    print(json.dumps(d, cls=HexJsonEncoder))
