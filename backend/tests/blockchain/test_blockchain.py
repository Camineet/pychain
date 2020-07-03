import sys
sys.path.append(".")
import pytest
from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.blockchain.block import Block, GENESIS_DATA

def test_blockchain_instance():
    # It should create a blockchain and test it
    blockchain = Blockchain()
    assert isinstance(blockchain, Blockchain)
    assert blockchain.chain[0].hash == GENESIS_DATA['hash']

def test_add_block():
    # It should add a block and test it
    blockchain = Blockchain()
    blockchain.add_block('foo')
    assert blockchain.chain[-1].data == 'foo'
    
@pytest.fixture
def blockchain_three_blocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block([Transaction(Wallet(), 'recipient', i).to_json()])
    return blockchain

def test_is_valid_chain(blockchain_three_blocks):
    Blockchain.is_valid_chain(blockchain_three_blocks.chain)
    
def test_is_valid_chain_bad_genesis(blockchain_three_blocks):
    blockchain_three_blocks.chain[0].hash = 'evil_hash'
    with pytest.raises(Exception, match='The genesis block is not valid'):
        Blockchain.is_valid_chain(blockchain_three_blocks.chain)
        
def test_replace_chain(blockchain_three_blocks):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_three_blocks.chain)
    
    assert blockchain.chain == blockchain_three_blocks.chain
    
def test_replace_chain_chain_not_longer(blockchain_three_blocks):
    blockchain = Blockchain()
    with pytest.raises(Exception, match='Cannot replace. The incoming chain must be longer than the local chain'):
        blockchain_three_blocks.replace_chain(blockchain.chain)
        
def test_replace_chain_bad_chain(blockchain_three_blocks):
    blockchain = Blockchain()
    blockchain_three_blocks.chain[1].hash = 'evil_hash'
    with pytest.raises(Exception, match='Cannot replace. The incoming chain is invalid'):
        blockchain.replace_chain(blockchain_three_blocks.chain)
        
def test_valid_transaction_chain(blockchain_three_blocks):
    Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)
    
def test_is_valid_transaction_chain_duplicate_transactions(blockchain_three_blocks):
    transaction = Transaction(Wallet(), 'recipient', 1).to_json()
    blockchain_three_blocks.add_block([transaction, transaction])
    with pytest.raises(Exception, match='is not unique'):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)
        
def test_is_valid_transaction_chain_duplicate_mining_rewards(blockchain_three_blocks):
    reward_1 = Transaction.reward_transaction(Wallet()).to_json()
    reward_2 = Transaction.reward_transaction(Wallet()).to_json()
    blockchain_three_blocks.add_block([reward_1, reward_2])
    with pytest.raises(Exception, match='There can only be one mining reward per block'):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)
    
def test_is_valid_transaction_chain_bad_transaction(blockchain_three_blocks):
    bad_transaction = Transaction(Wallet(), 'recipient', 1)
    bad_transaction.input['signature'] = Wallet().sign(bad_transaction.output)
    blockchain_three_blocks.add_block([bad_transaction.to_json()])
    
    with pytest.raises(Exception):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)
        
def test_is_valid_transaction_chain_bad_historic_balance(blockchain_three_blocks):
    wallet = Wallet()
    bad_transaction = Transaction(wallet, 'recipient', 1)
    # don't understand the point of this line of code. the point of the test is to ensure bad data isn't entered into the input['amount'] field which would result in the sender wallet's balance getting inflated. altering the output[wallet.address] field only serves to change the signature result, as far as i can tell. the test even passes when commenting out this line of code.
    bad_transaction.output[wallet.address] = 9000
    bad_transaction.input['amount'] = 9001
    bad_transaction.input['signature'] = wallet.sign(bad_transaction.output)
    
    blockchain_three_blocks.add_block([bad_transaction.to_json()])
    
    with pytest.raises(Exception, match='has invalid input amount'):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)
    
    