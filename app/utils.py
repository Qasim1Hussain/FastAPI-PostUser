from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash(password: str) ->str:
    return password_hash.hash(password)

def varify(plain_password, hash_password):
    return password_hash.verify(plain_password, hash_password)