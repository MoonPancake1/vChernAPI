import random
import string


def get_code_verifier():
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(64)])