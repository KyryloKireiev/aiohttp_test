import bcrypt


def generate_hash(password):
    password_bin = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bin, bcrypt.gensalt())
    return hashed.decode("utf-8")


def get_test_merge_conflict():
    print("Try to make conflict")
