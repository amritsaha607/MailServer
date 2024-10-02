from mailing.models import RawEvent


def save_event(event):
    event = RawEvent(
        chain_id=event.get('id'),
        payload=event
    )
    event.save()
    print(f'RawEvent {event.id}, {event.chain_id} saved successfully')
    return event.chain_id
