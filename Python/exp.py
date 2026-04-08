#hash = "00252ef9428c8c4109219ac6ec3e1b9727868a44a31c3850aeaa4a76b0031bb0"
#print(str('0' * 7))
#print(hash.startswith(str('0' * 2)))
#print(hash.startswith(str('0' * 2))==False)

from ecdsa import SigningKey, SECP256k1
# --- 1. Generate a Private Key ---
# A private key is just a random number between 1 and the curve's order
private_key = SigningKey.generate(curve=SECP256k1)
print(type(private_key))
print("Private Key (hex):", private_key.to_string().hex())