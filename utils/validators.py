from utils.exceptions import ValidationException


def validate_attr_present(payload: dict, attr_name: any, logger_key: str):

    if isinstance(attr_name, list) or isinstance(attr_name, dict):
        for attr in attr_name:
            if not validate_attr_present(payload, attr, logger_key):
                raise ValidationException(
                    f'{logger_key}Attribute {attr} not present in payload')
        return True

    return payload.__contains__(attr_name)


def validate_attr_type(payload: dict, attr_name_type_mapping: dict, logger_key: str):
    for attr_name, attr_type in attr_name_type_mapping.items():
        if not isinstance(payload.get(attr_name), attr_type):
            raise ValidationException(
                f'{logger_key}Attribute {attr_name} is not of type {attr_type}')
