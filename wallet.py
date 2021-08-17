# Import dependencies
import subprocess
import json
import os
from web3 import Web3
from eth_account import Account
import bit
from bit import PrivateKeyTestnet
from constants import *
#from dotenv import load_dotenv

# Load and set environment variables
load_dotenv()
mnemonic = os.getenv("mnemonic")


# Import constants.py and necessary functions from bit and web3
#from bit import wif_to_key
from constants import *
import subprocess
import json

"""This method executed the HD wallet call in commad =line and parses the output in json
   format and returns it to caller
"""
def derive_wallets(coin,mnemonic):  
    command = 'php derive -g --mnemonic="'+mnemonic+'" --cols=path,address,privkey,pubkey --format=json --coin='+ coin 
    print (command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)


# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {}
coins[ETH] = derive_wallets(ETH,mnemonic)
coins[BTCTEST] = derive_wallets(BTCTEST,mnemonic)
print(coins)

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin_prev_key, coin):  # YOUR CODE HERE):
    if coin == ETH:
        return Account.from_key(coin_prev_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(coin_prev_key)
    else:
        return None


# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin,account,to,amount):  
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas({"from":account.address,"to":recipient,"value":amount})
        raw_tx = {}
        raw_tx['from'] = account.address
        raw_tx['to'] = recipient
        raw_tx['value'] = amount
        raw_tx['gasPrice'] = w3.eth.gasPrice
        raw_tx['gas'] = gasEstimate
        raw_tx['chainId'] = 777
        raw_tx['nonce'] = w3.eth.getTransactionCount(account.address)
        return raw_tx
    elif coin == BTCTEST:
        raw_tx = PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount,BTC)])
        return raw_tx
    else:
        return None
        
# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin,account,to,amount):  
    if coin == ETH:
        tx = create_tx(coin,account,to,amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return result
    elif coin == BTCTEST:
        tx = create_tx(coin,account,to,amount)
        signed_tx = account.sign_transaction(tx)
        result = NetworkAPI.broadcast_tx_testnet(signed)
    else:
        return None

account = priv_key_to_account(coins[BTCTEST][0]['privkey'],BTCTEST)
print (account)
#Before using it ensure the account has been funded with bit coin 
result = send_tx(BTCTEST,account,'0x98103b6C1134F359733CfE3aDe856c728DF023d2',1)                                                 
                                                     
                                                     
                                                     
        
                                                     
                                                     
                                                     
                                                     
                                                     