import bcrypt

print(bcrypt.hashpw("admin".encode("utf-8") ,bcrypt.gensalt() ) )