import json

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from mailing.constants import COMPOSE_MAIL_PAYLOAD_ATTRIBUTES
from mailing.handlers import handle_failure_api
from mailing.views.event_manager import save_event
from utils.validators import validate_attr_present


@method_decorator(csrf_exempt, name='dispatch')
class ComposeMailView(View):
    def validate_mail(self, data, logger_key):
        validate_attr_present(
            payload=data,
            attr_name=COMPOSE_MAIL_PAYLOAD_ATTRIBUTES,
            logger_key=logger_key
        )

    @method_decorator(handle_failure_api)
    def post(self, request):
        data = json.loads(request.body)
        event_id = save_event(data)

        logger_key = f'Compose Mail {event_id}: '
        self.validate_mail(data, logger_key)

        return
