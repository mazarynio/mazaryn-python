import uuid
from profiles.models import Profile


def get_random_code():
    code = str(uuid.uuid4())[:5].replace('-', '').lower()
    return code


def validate_email(email):
    profile = None
    try:
        profile = Profile.objects.get(email=email)
    except Profile.DoesNotExist:
        return None

    if profile != None:
        return email


# def validate_username(username):
#     profile = None
#     try:
#         profile = Profile.objects.get(username=username)
#     except Profile.DoesNotExist:
#         return None

#     if profile != None:
#         return username
