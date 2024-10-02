from mailing.models import User
from mailing.querysets.users import get_user_by_email
from mailing.utils import sha512
from utils.exceptions import NotFoundException


def create_user_from_json(data: dict) -> User:
    user = User()
    user.name = data.get('name')
    user.email = data.get('email')
    user.dob = data.get('dob')

    if data.get('password') is not None:
        user.password = sha512(data.get('password'))

    return user


def validate_email_and_get_user(email, context='') -> User:
    user = get_user_by_email(email)
    if user is None:
        raise NotFoundException(
            f'{context} - User not found for email {email}')
    return user


def get_user_context_logkey(email):
    return f'Email: {email}'
