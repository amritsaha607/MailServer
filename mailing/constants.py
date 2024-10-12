from datetime import date, datetime

COMPOSE_MAIL_PAYLOAD_ATTRIBUTES = {
    'id': str,
    'sender': str,
    'receivers': list,
    'subject': str,
    'content': str,
    'timestamp': str | datetime | date,
}

FETCH_MAIL_PAYLOAD_ATTRIBUTES = {
    'ids': str | list,
    'senders': str | list,
    'receivers': str | list,
}
