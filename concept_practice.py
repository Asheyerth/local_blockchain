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
        self.hash = self.calculate_hash() # Calculate the block's own hash

    def calculate_hash(self):
        # Concatenate block data and hash it using SHA-256
        block_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) #the hash is done with the id, time, message and previous hash
        return hashlib.sha256(block_string.encode()).hexdigest() #that is returned in a sha256

# Define the Blockchain
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()] # Initialize the chain with a genesis block

    def create_genesis_block(self):
        # The first block, which has no previous hash
        return Block(0, datetime.now(), "Genesis Block", "0") #return a default block. I don't see this in real examples

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        # Link the new block to the previous block using its hash
        new_block.previous_hash = self.get_latest_block().hash #when added a new block, it needs to be chained to the last one already existing
        new_block.hash = new_block.calculate_hash() #the hash is calculated after the new block is created
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