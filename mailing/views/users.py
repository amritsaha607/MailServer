import json
import logging

from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from mailing.handlers import handle_failure_api
from mailing.helper import (create_user_from_json, get_user_context_logkey,
                            validate_email_and_get_user)
from mailing.querysets.users import get_user, get_user_by_email
from mailing.utils import get_json_data, sha512
from utils.exceptions import ValidationException


@method_decorator(csrf_exempt, name='dispatch')
class UsersView(View):

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
        context = get_user_context_logkey(email)

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
        context = get_user_context_logkey(email)

        self.validate_create(email, context)

        user = create_user_from_json(data)
        user.created_at = timezone.now()
        user.updated_at = timezone.now()
        logging.info(f'{context} - User created')

        user.save()

        return JsonResponse(get_json_data(user, context))

    @method_decorator(handle_failure_api)
    def put(self, request):
        data = json.loads(request.body)

        email = data.get('email')
        context = get_user_context_logkey(email)

        user = validate_email_and_get_user(email, context)

        if data.get('name') is not None:
            user.name = data.get('name')
        if data.get('dob') is not None:
            user.dob = data.get('dob')
        user.updated_at = timezone.now()

        logging.info(f'{context} - User updated')

        user.save()

        return JsonResponse(get_json_data(user, context))


class AuthView(View):

    def validate_create(self, email, context=''):
        if get_user_by_email(email) is not None:
            raise ValidationException(f'{context} - email already exists')

    def validate_mode(self, mode, context=''):
        if mode != 'login' and mode != 'signup':
            raise ValidationException(f'{context} - Invalid mode {mode}')

    def login(self, email, password, context=''):
        user = get_user_by_email(email)
        if user is None or user.password != sha512(password):
            raise ValidationException(f'{context} - Invalid Credentials')
        return user

    def signup(self, data):
        user = create_user_from_json(data)
        user.created_at = timezone.now()
        user.updated_at = timezone.now()
        return user

    @method_decorator(handle_failure_api)
    def post(self, request):
        data = json.loads(request.body)

        mode = data.get('auth_mode')
        email = data.get('email')
        password = data.get('password')
        context = get_user_context_logkey(email)

        self.validate_mode(mode, context)

        if mode == 'login':
            user = self.login(email, password, context)
        elif mode == 'signup':
            self.validate_create(email, context)
            user = self.signup(data)
            user.save()
            logging.info(f'{context} - User created')

        return JsonResponse(get_json_data(user, context))
