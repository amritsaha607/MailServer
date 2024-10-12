from utils.constants import VALIDATE_MODE_AND, VALIDATE_MODE_OR
from utils.exceptions import ValidationException


def validate_attr_present(payload: dict, attr_name: any, logger_key: str):

    if isinstance(attr_name, list) or isinstance(attr_name, dict):
        for attr in attr_name:
            validate_attr_present(payload, attr, logger_key)
        return True

    if not payload.__contains__(attr_name):
        raise ValidationException(
            f'{logger_key}Attribute {attr_name} not present in payload')

    return True


def validate_attr_type(payload: dict, attr_name_type_mapping: dict, logger_key: str):
    for attr_name, attr_type in attr_name_type_mapping.items():
        # Skip attributes not present
        if not payload.__contains__(attr_name):
            continue

        if not isinstance(payload.get(attr_name), attr_type):
            raise ValidationException(
                f'{logger_key}Attribute {attr_name} is not of type {attr_type}')
