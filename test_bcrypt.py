import bcrypt
password = "test"
hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
print(f"Hash: {hash}")
is_valid = bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))
print(f"Valid: {is_valid}")
