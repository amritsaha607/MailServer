from mailing.models import User

from .utils import get_or_none


def get_user(user_id) -> User:
    user_or_none = User.objects.filter(id=user_id)
    return get_or_none(user_or_none)


def get_user_by_email(email) -> User:
    user_or_none = User.objects.filter(email=email)
    return get_or_none(user_or_none)


def search_user_emails_by_email_query(query) -> list:
    emails_qset = User.objects.filter(
        email__contains=query).values_list('email', flat=True)
    return list(emails_qset)
