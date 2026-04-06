import hashlib
#import time
from datetime import datetime


# Define the Block structure
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index #id
        self.timestamp = timestamp #time
        self.data = data #message
        self.previous_hash = previous_hash #hash of the previous block
        self.nonce = 0 #Proof of work
        self.hash = self.calculate_hash() # Calculate the block's own hash

    def calculate_hash(self):
        # Concatenate block data and hash it using SHA-256
        block_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce) #the hash is done with the id, time, message and previous hash
        return hashlib.sha256(block_string.encode()).hexdigest() #that is returned in a sha256

    def mine(self, difficulty): #Proof of work 
        # Basically, it loops until our hash starts with 
        # the string 0...000 with length of <difficulty>.
        while (self.hash.startswith(str('0' * difficulty))==False):
            # We increases our nonce so that we can get a whole different hash.
            self.nonce+= 1
            # Update our new hash with the new nonce value.
            self.hash = self.calculate_hash()
        
    

# Define the Blockchain
class Blockchain:
    def __init__(self):
        self.difficulty = 5
        self.chain = [self.create_genesis_block()] # Initialize the chain with a genesis block

    def create_genesis_block(self):
        # The first block, which has no previous hash
        genesis = Block(0, datetime.now(), "Genesis Block", "0")
        genesis.mine(self.difficulty)
        return genesis #return a default block. I don't see this in real examples

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        # Link the new block to the previous block using its hash
        new_block.previous_hash = self.get_latest_block().hash #when added a new block, it needs to be chained to the last one already existing
        new_block.hash = new_block.calculate_hash() #the hash is calculated after the new block is created
        new_block.mine(self.difficulty) #for Proof of work. Find the nonce
        self.chain.append(new_block) #the new block is chained to the chain 

    def is_chain_valid(self):
        # Validate the chain integrity by checking the hash links
        for i in range(1, len(self.chain)): #for every block in the chain 
            current_block = self.chain[i] #iteration temp
            previous_block = self.chain[i-1] #iteration temp

            #if somehow fails the hash, then its not valid
            #when something changed, the hash changes, therefore the validate with private keys and another blocks fails
            #this comparison actually happens with another nodes when the same information its stored 
            if current_block.hash != current_block.calculate_hash(): #the block of the current node vs the block of another node 
                return False

            if current_block.previous_hash != previous_block.hash: #same with previous
                return False

        return True

    #See the chain
    def print_chain(self):
        for i in range(0, len(self.chain)):
            current_block = self.chain[i]
            print("index")
            print(current_block.index)
            print("timestamp")
            print(current_block.timestamp)
            print('data')
            print(current_block.data)
            print('hash')
            print(current_block.hash)

# Example Usage (refer to source links for full implementation):
if __name__ == "__main__":
    my_blockchain = Blockchain()
    print("Mining block 1...")
    my_blockchain.add_block(Block(1, datetime.now(), {"amount": 4, "sender": "Alice", "recipient": "Bob"}, ""))
    print("Mining block 2...")
    my_blockchain.add_block(Block(2, datetime.now(), {"amount": 8, "sender": "Bob", "recipient": "Alice"}, ""))
    my_blockchain.print_chain()
    
    # Check if the chain is valid
    print("Is Blockchain Valid?", my_blockchain.is_chain_valid())


#Server part #########################################################
# Flask is for creating the web
# app and jsonify is for
# displaying the blockchain
from flask import Flask, jsonify

# Creating the Web
# App using flask
app = Flask(__name__)

# Create the object
# of the class blockchain
blockchain = Blockchain()

# Mining a new block


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_latest_block() #Get the last block 
    print(blockchain.print_chain())
    #previous_proof = previous_block['proof'] #Get the nonce of the last block 
    #proof = blockchain.proof_of_work(previous_proof) #get the hash hash of the previous block I think 
    #previous_hash = blockchain.hash(previous_block) #I think... 
    #block = blockchain.create_block(proof, previous_hash) #Add a new block with the nonce and previous hash. I dont know why the nonce

    #Well... add a new one, I think ¿?
    new_block = Block(len(blockchain.chain), datetime.now(), {"amount": 12, "sender": "Charlie", "recipient": "Bob"}, "")
    blockchain.add_block(new_block)

    response = {'message': 'A block is MINED',
                'index': new_block.index,
                'timestamp': new_block.timestamp,
                'proof': new_block.nonce,
                'previous_hash': new_block.previous_hash}

    return jsonify(response), 200

# Display blockchain in json format


@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {'chain': str(blockchain.chain),
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Check validity of blockchain


@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.is_chain_valid()

    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200


# Run the flask server locally
app.run(host='127.0.0.1', port=5000)