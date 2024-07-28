from mailing.models import User

from .utils import get_or_none


def get_user(user_id) -> User:
    user_or_none = User.objects.filter(id=user_id)
    return get_or_none(user_or_none)


def get_user_by_email(email) -> User:
    user_or_none = User.objects.filter(email=email)
    return get_or_none(user_or_none)
