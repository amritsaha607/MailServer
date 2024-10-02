import logging

from mailing.models import RawEvent

logger = logging.getLogger(__name__)


def save_event(event):
    event = RawEvent(
        chain_id=event.get('id'),
        payload=event
    )
    event.save()
    logger.info(f'RawEvent {event.id}, {event.chain_id} saved successfully')
    return event.chain_id
