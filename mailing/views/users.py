import json
import logging

from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from mailing.exceptions import ValidationException
from mailing.handlers import handle_failure_api
from mailing.helper import create_user_from_json
from mailing.querysets.users import get_user, get_user_by_email
from mailing.utils import get_json_data


@method_decorator(csrf_exempt, name='dispatch')
class UsersView(View):

    def get_context(self, user_id, email):
        return f'user_id: {user_id}, email: {email}'

    def validate_get(self, user_id, email, context=''):
        if user_id is None and email is None:
            raise ValidationException(
                f"{context} - Please provide user id or email")

    def validate_create(self, email, context=''):
        if get_user_by_email(email) is not None:
            raise ValidationException(f'{context} - email already exists')

    @method_decorator(handle_failure_api)
    def get(self, request):
        params = request.GET

        user_id = params.get('user_id')
        email = params.get('email')
        context = self.get_context(user_id, email)

        self.validate_get(user_id, email, context)

        if user_id is not None:
            user = get_user(user_id)
        else:
            user = get_user_by_email(email)

        return JsonResponse(get_json_data(user, context))

    @method_decorator(handle_failure_api)
    def post(self, request):
        data = json.loads(request.body)

        email = data.get('email')
        context = self.get_context('', email)

        self.validate_create(email, context)

        user = create_user_from_json(data)
        user.created_at = timezone.now()
        user.updated_at = timezone.now()
        logging.info(f'{context} - User created')

        user.save()

        return JsonResponse(get_json_data(user, context))
