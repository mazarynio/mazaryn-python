import uuid


def get_random_code():
    return str(uuid.uuid4())[:5].replace('-', '').lower()  # return code
