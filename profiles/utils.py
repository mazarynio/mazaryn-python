import uuid
from profiles import models



def get_random_code():
    code = str(uuid.uuid4())[:5].replace('-', '').lower()
    return code

