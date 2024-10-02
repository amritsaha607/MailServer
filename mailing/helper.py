from mailing.models import MailEvent, User
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


def create_mail_event_from_payload(payload: dict, logger_key) -> MailEvent:
    sender_email = payload.get('sender')
    sender = validate_email_and_get_user(sender_email, logger_key)

    receivers = payload.get('receivers')
    receivers = [validate_email_and_get_user(
        email, logger_key) for email in receivers]

    mail_event = MailEvent(
        chain_id=payload.get('id'),
        subject=payload.get('subject'),
        content=payload.get('content'),
        sender=sender,
        sent_at=payload.get('timestamp'),
    )
    mail_event.save()

    mail_event.receivers.set(receivers)
    return mail_event
