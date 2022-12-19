import bcrypt


def generate_password_hash(password):
    password_bin = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bin, bcrypt.gensalt())
    return hashed.decode("utf-8")
