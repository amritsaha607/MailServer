import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from mailing.constants import (COMPOSE_MAIL_PAYLOAD_ATTRIBUTES,
                               FETCH_MAIL_PAYLOAD_ATTRIBUTES)
from mailing.handlers import handle_failure_api
from mailing.helper import (create_mail_event_from_payload,
                            create_mail_items_from_event)
from mailing.models import MailEvent
from mailing.querysets.mail_events import get_mail_event
from mailing.querysets.mails import filter_emails
from mailing.views.event_manager import save_event
from utils.constants import VALIDATE_MODE_AND, VALIDATE_MODE_OR
from utils.exceptions import DuplicateRequestException
from utils.validators import validate_attr_present, validate_attr_type


class ComposeMailView(View):
    def validate_attributes(self, data, logger_key: str):
        validate_attr_present(
            payload=data,
            attr_name=COMPOSE_MAIL_PAYLOAD_ATTRIBUTES,
            validation_mode=VALIDATE_MODE_AND,
            logger_key=logger_key
        )
        validate_attr_type(
            payload=data,
            attr_name_type_mapping=COMPOSE_MAIL_PAYLOAD_ATTRIBUTES,
            logger_key=logger_key
        )

    def validate_mail_event_not_present(self, chain_id, logger_key: str):
        if get_mail_event(chain_id) is not None:
            raise DuplicateRequestException(f'{logger_key}MailEvent exists')

    def create_mail_event(self, payload, logger_key: str):
        return create_mail_event_from_payload(payload, logger_key)

    def create_mail_items(self, mail_event: MailEvent, logger_key: str):
        return create_mail_items_from_event(mail_event, logger_key)

    @method_decorator(handle_failure_api)
    def post(self, request):
        data = json.loads(request.body)
        chain_id = save_event(data)

        logger_key = f'Compose Mail {chain_id}: '

        # Validate all required attributes are present
        self.validate_attributes(data, logger_key)

        # For composing new email, check if chain_id already exists for MailEvents.
        # if yes, it's a duplicate/invalid request
        self.validate_mail_event_not_present(chain_id, logger_key)

        # Create & save mail event
        mail_event = self.create_mail_event(data, logger_key)
        mail_event.save()

        # trigger mail creation job
        self.create_mail_items(mail_event, logger_key)

        return JsonResponse(mail_event.get_json_data())


@method_decorator(csrf_exempt, name='dispatch')
class FetchMailView(View):

    def validate_attributes(self, data, logger_key: str):
        validate_attr_present(
            payload=data,
            attr_name=FETCH_MAIL_PAYLOAD_ATTRIBUTES,
            validation_mode=VALIDATE_MODE_OR,
            logger_key=logger_key
        )
        validate_attr_type(
            payload=data,
            attr_name_type_mapping=FETCH_MAIL_PAYLOAD_ATTRIBUTES,
            logger_key=logger_key
        )

    @method_decorator(handle_failure_api)
    def post(self, request):

        data = json.loads(request.body)
        logger_key = f'Fetch Mail {data}: '

        self.validate_attributes(data, logger_key)

        ids = data.get('ids')
        senders = data.get('senders')
        receivers = data.get('receivers')

        mails = filter_emails(ids, senders, receivers)

        return JsonResponse([mail.get_json_data() for mail in mails], safe=False)
