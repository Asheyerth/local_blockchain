import hashlib
#import time
from datetime import datetime
import json
from enum import Enum
from ecdsa import SigningKey, VerifyingKey, SECP256k1

#Dummy information for basic usage
#This should be a database call or .env/config.json 
users = {
    "Ana" : "ana",
    "Bill" : "bill",
    "Chris" : "chris",
    "Danny" : "danny"
}
secretKeys = {
    "Ana" : "e8c6ff837053d551e98db92f9fbac904fbcc71405287616053eee4d51f703ed6",
    "Bill" : "2e31928a752ef161f83071831ab878094349226f4b3aed082ac31bcfbab69010",
    "Chris" : "1153f33cfff9581e9a33dd82cb68dba5ca2bac990ef907edaf829eb9bcd38815",
    "Danny" : "ad50627cae83bd60d609f440e8ae9f53b97021265cb5e9d4afbe19d3654f3134"
}
publicKeys = {
    "Ana" : "a99a1adc81c9388b2ddf084ae5a685878130aa6607f96a9ee302d8109ccbc46ebda52f92922ce831ad621f349a78676cdcc4685aefa85d7e97b24b7c181c11b5",
    "Bill" : "60a9f4426d330e8b4a1df01597b0cc8193b3f62810ccc9f429a7ff15b956b3c4d175ec1e0b1c85d6d4ec7e4758f0c5bcc8345e1025cff4ecabb2e12fdc28794d",
    "Chris" : "17b149a9522468c02e64cd466018e62030ae60e13840bb152844701ec30128c70d804ae240eeb46d23fb028619ce14b3df7586a3d364607627da2f8d227ebc15",
    "Danny" : "caeb7d60cba24e7c854a4fa68ed53c557478458c488d21e1ebdbc53c659bd1b13185b2f782355c543a7ef5bad5807023ec7450d653bde0083a8a217cbc5002cd"
}
    

# Define the Transaction structure
class Transaction: 
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = ""

    def signTransaction(self, private_key_hex): #public_key_hex = publicKeys[session['user']]
        #Making it JSON
        #message = {
        #        "sender": self.sender,
        #        "recipient": self.recipient,
        #        "amount": str(self.amount)}
        #message = b"Hello, Blockchain!"
        #messageBytes = json.dumps(message).encode('utf-8')

        # --- Sender's private key (as bytes) ---
        private_key_bytes = bytes.fromhex(private_key_hex)
        private_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)

        # --- Transaction object (as bytes) ---
        #transaction = b"{\"nonce\":0,\"to\":\"0xRecipient\",\"value\":1000000000000000000,\"gas\":21000}"  # Simplified
        #transaction_hash = hashlib.sha256(messageBytes).digest()
        message = {
                "sender": self.sender,
                "recipient": self.recipient,
                "amount": str(self.amount)}
        #message = b"Hello, Blockchain!"
        messageBytes = json.dumps(message).encode('utf-8')

        # --- Sign the transaction ---
        signature = private_key.sign(messageBytes, hashfunc=hashlib.sha256)

        print("Signed Transaction (hex):", signature.hex())
        self.signature = signature
        return signature.hex()
    
    def verifyTransaction(self, signature, public_key_hex):
        print("verification")
        print(self.sender)
        print(self.recipient)
        print(self.amount)
        print(signature)
        # --- Sender's public key (as bytes) ---
        public_key_bytes = bytes.fromhex(public_key_hex)
        public_key = VerifyingKey.from_string(public_key_bytes, curve=SECP256k1)

        # --- Transaction object (as bytes) ---
        #transaction = b"{\"nonce\":0,\"to\":\"0xRecipient\",\"value\":1000000000000000000,\"gas\":21000}"
        #transaction_hash = hashlib.sha256(transaction).digest()
        message = {
                "sender": self.sender,
                "recipient": [self.recipient],
                "amount": str(self.amount)}
        #message = b"Hello, Blockchain!"
        messageBytes = json.dumps(message).encode('utf-8')
        print(message)

        # --- Verify the signature ---
        try:
            public_key.verify(signature, messageBytes, hashfunc=hashlib.sha256)
            self.signature = signature
            print("✅ Signature is valid! The sender owns the private key.")
            return True
        except:
            print("❌ Signature is invalid!")
            return False
        




# Define the Block structure
class Block:
    def __init__(self, index, transactions, previous_hash):
        print("asdadasdasdasdasadadasdasdasdasd")
        self.index = index #id
        self.timestamp = datetime.now() #time
        #self.data = data #message
        #self.transaction = transaction #message
        self.previous_hash = previous_hash #hash of the previous block
        self.nonce = 0 #Proof of work
        self.hash = self.calculate_hash() # Calculate the block's own hash
        self.current_transactions = transactions # Reset the current list of transactions

    def calculate_hash(self):
        # Concatenate block data and hash it using SHA-256
        ####################################ADD TRANSACTIONS
        block_string = str(self.index) + str(self.timestamp) + str(self.previous_hash) + str(self.nonce) #the hash is done with the id, time, message and previous hash
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
        print("ASDASDASDSADASDASDASDASDASDASDASDASDSAASD")
        self.chain = [self.create_genesis_block()] # Initialize the chain with a genesis block

    def create_genesis_block(self):
        # The first block, which has no previous hash
        genesis = Block(0, "Genesis Block", "0")
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

    #Add new transaction to the block
    def new_transaction(self, sender, recipient, amount):
        new_transaction = Transaction(sender, recipient, amount)
        self.current_transactions.append(new_transaction)

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
        data = []
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
            data.append({
                "index": str(current_block.index),
                "timestamp": str(current_block.timestamp),
                "data": str(current_block.data),
                "hash": str(current_block.hash)})
        json_string = json.dumps(data, indent=4)
        return json_string

# Example Usage (refer to source links for full implementation):
#if __name__ == "__main__":
#    my_blockchain = Blockchain()
#    print("Mining block 1...")
#    my_blockchain.add_block(Block(1, {"amount": 4, "sender": "Alice", "recipient": "Bob"}, ""))
#    print("Mining block 2...")
#    my_blockchain.add_block(Block(2, {"amount": 8, "sender": "Bob", "recipient": "Alice"}, ""))
#    my_blockchain.print_chain()
    
    # Check if the chain is valid
#    print("Is Blockchain Valid?", my_blockchain.is_chain_valid())


#Server part #########################################################
# Flask is for creating the web
# app and jsonify is for
# displaying the blockchain
from flask import Flask, jsonify, request, redirect, url_for, session, render_template

# Creating the Web
# App using flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session

# Create the object
# of the class blockchain
blockchain = Blockchain()


@app.route('/')
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

#Login 
@app.route('/login', methods=['POST'])
def handle_login():
    print("login")
    if request.method == 'POST':
        print("post")
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['user'] = username
            print("yes")
            return redirect(url_for('dashboard'))
        else:
            print("no")
            return render_template('login.html')

# Mining a new block
@app.route('/mine_block', methods=['POST'])
def mine_block():
    print("mine")
    data = request.get_json()
    print(data)
    addTOblock = []
    #1. Collecting Transactions
    ##Get the form of the HMTL here
    listTransaction = data.get("listTransaction")
    print(type(listTransaction))
    listTransactions = listTransaction.split(";") 
    listTransactions.pop()
    print(listTransactions)
    for trans in listTransactions:
        print("asdad")
        print(trans)
        atributesTrans = trans.split(",")
        #signatureVerify = atributesTrans[3]
        #signatureTOverify = signatureVerify[signatureVerify.find(":")+2:-2]
        #Verify the signature
        print("Atributes")
        sender = atributesTrans[0][atributesTrans[0].find(":")+2:-1]
        recipient = atributesTrans[1][atributesTrans[1].find(":")+3:-2]
        amount = atributesTrans[2][atributesTrans[2].find(":")+2:-1]
        signatureTOverify = atributesTrans[3][atributesTrans[3].find(":")+2:-2]
        #print(atributesTrans[0][atributesTrans[0].find(":")+2:-1])
        #print(atributesTrans[1][atributesTrans[1].find(":")+3:-2])
        #print(atributesTrans[2][atributesTrans[2].find(":")+2:-1])
        #print(atributesTrans[3][atributesTrans[3].find(":")+2:-2])
        new_transaction = Transaction(sender, recipient, amount)
        public_key_hex = publicKeys[session['user']] #Lets imagine this is properly getted 
        verified = new_transaction.verifyTransaction(signatureTOverify,public_key_hex)
        if (verified): #if its verified
            addTOblock.append(new_transaction)
        #else{
        #    response = {'message': "Not verified"}
        #    return jsonify(response), 200
        #}

    #2. Building the Block and getting the Proof of Work 
    #Well... add a new one, I think ¿?
    new_block = Block(len(blockchain.chain), addTOblock, "")
    blockchain.add_block(new_block)

    #3. Broadcasting 
    response = {'message': 'A block is MINED',
                'index': new_block.index,
                'timestamp': new_block.timestamp,
                'proof': new_block.nonce,
                'previous_hash': new_block.previous_hash,
                'hash':new_block.hash,
                'transactions': new_block.current_transactions}

    return jsonify(response), 200

#Sign the transaction
@app.route('/signTransaction', methods=['POST'])
def signTransactionHandler():
    print("entra sign")
    data = request.get_json()
    sender = data.get('sender')
    recipient = data.get('recipient')
    amount = data.get("amount")
    new_transaction = Transaction(sender, recipient, amount)
    #Let's believe that the privateKey is taken from a safe space or something
    signature = new_transaction.signTransaction(secretKeys[session['user']])
    response = {'message': "Signed",
                "signature" : signature}
    return jsonify(response), 200


# Display blockchain in json format
@app.route('/get_chain', methods=['GET'])
def display_chain():
    #for visualization
    #strPrint = blockchain.print_chain()
    #print(strPrint)
    response = {'chain': blockchain.print_chain(),
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