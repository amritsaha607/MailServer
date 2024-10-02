from mailing.models import RawEvent


def save_event(event):
    event = RawEvent(payload=event)
    event.save()
    print(f'RawEvent {event.id} saved successfully')
    return event.id
