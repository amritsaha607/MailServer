import hashlib

from django.http import JsonResponse

from mailing.exceptions import NotFoundException


def getInfoFromPartial(partialMethod):
    return f"{partialMethod.func.__self__.__class__.__name__}.{partialMethod.func.__name__}"


def get_json_data(object_or_none, context=''):
    if object_or_none is None:
        raise NotFoundException(f'{context} - Data not found')

    return object_or_none.get_json_data()


def get_json_response(message, status=200):
    return JsonResponse({
        "message": message,
    }, safe=False, status=status)


def sha512(password):
    return hashlib.sha512(password.encode('utf-8')).hexdigest()
