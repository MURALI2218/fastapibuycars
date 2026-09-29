
from pwdlib import PasswordHash
password_hash = PasswordHash.recommended()

def hash_password(password : str):
    return password_hash.hash(password)

def verify_password(entered_password, dbpassword):
    return password_hash.verify(entered_password, dbpassword)

