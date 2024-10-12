from mailing.models import MailEvent

from .utils import get_or_none


def get_mail_event(chain_id: str):
    mail_event_or_none = MailEvent.objects.filter(chain_id=chain_id)
    return get_or_none(mail_event_or_none)
