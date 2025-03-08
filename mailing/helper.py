import logging
from copy import deepcopy

from mailing.models import MailEvent, MailItem, User
from mailing.querysets.users import get_user_by_email
from mailing.utils import sha512
from utils.exceptions import NotFoundException

logger = logging.getLogger(__name__)


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

    receivers = list(set([receiver.strip()
                     for receiver in payload.get('receivers')]))
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


def create_mail_item(mail_draft: MailItem, user: User):
    mail_item = deepcopy(mail_draft)
    mail_item.user = user
    return mail_item


def create_mail_items_from_event(mail_event: MailEvent, logger_key: str):
    logger.info(f'{logger_key}START: Creating mailItems')
    mail_draft = MailItem(
        chain_id=mail_event.chain_id,
        event=mail_event,
        timestamp=mail_event.sent_at,
    )

    sender = mail_event.sender
    receivers = mail_event.receivers.all()

    n_items = receivers.count() + 1

    logger.info(
        f'{logger_key}Creating {n_items} mailItems')

    mail_items = [create_mail_item(mail_draft, user)
                  for user in [sender, *receivers]]

    mail_items = MailItem.objects.bulk_create(mail_items)
    logger.info(
        f'{logger_key}END: Created {n_items} mailItems')

    return mail_items
