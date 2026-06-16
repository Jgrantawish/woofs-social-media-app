from pwdlib import PasswordHash


# Use the most modern hashing algorith to hash the user's password 
hashing_algorith = PasswordHash.recommended()

# Return the hash of the password passed in
def hash_password(password: str):
    return hashing_algorith.hash(password)
