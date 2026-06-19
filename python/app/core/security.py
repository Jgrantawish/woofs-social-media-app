from pwdlib import PasswordHash

# Use the most modern hashing algorith to hash the user's password 
hashing_algorithm = PasswordHash.recommended()

# Return the hash of the password passed in
def hash_password(password: str):
    return hashing_algorithm.hash(password)

# Verify the password against stored hash
def verify_password(password: str, password_hash: str) -> bool:
    return hashing_algorithm.verify(password, password_hash)
