from utils.constants import VALIDATE_MODE_AND, VALIDATE_MODE_OR
from utils.exceptions import ValidationException


def is_attr_present(payload: dict, attr_name: int | str):
    return payload.__contains__(attr_name)


def validate_attr_present(payload: dict, attr_name: list | dict, validation_mode: str, logger_key: str):

    if validation_mode.upper() == VALIDATE_MODE_AND:
        for attr in attr_name:
            if not is_attr_present(payload, attr):
                raise ValidationException(
                    f'{logger_key}Attribute {attr} not present in payload')
        return True

    elif validation_mode.upper() == VALIDATE_MODE_OR:
        for attr in attr_name:
            if is_attr_present(payload, attr):
                return True
        raise ValidationException(
            f'{logger_key}Attribute {attr} not present in payload')

    raise ValidationException(f'Invalid validation_mode: {validation_mode}')


def validate_attr_type(payload: dict, attr_name_type_mapping: dict, logger_key: str):
    for attr_name, attr_type in attr_name_type_mapping.items():
        # Skip attributes not present
        if not is_attr_present(payload, attr_name):
            continue

        if not isinstance(payload.get(attr_name), attr_type):
            raise ValidationException(
                f'{logger_key}Attribute {attr_name} is not of type {attr_type}')
