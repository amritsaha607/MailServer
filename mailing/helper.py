from mailing.models import User
from mailing.utils import sha512


def create_user_from_json(data: dict) -> User:
    user = User()
    user.name = data.get('name')
    user.email = data.get('email')
    user.dob = data.get('dob')

    if data.get('password') is not None:
        user.password = sha512(data.get('password'))

    return user
