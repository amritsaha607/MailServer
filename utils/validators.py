from utils.exceptions import ValidationException


def validate_attr_present(payload: dict, attr_name: any, logger_key: str):

    if isinstance(attr_name, list):
        for attr in attr_name:
            if not validate_attr_present(payload, attr, logger_key):
                raise ValidationException(
                    f'{logger_key}Attribute {attr} not present in payload')
        return True

    return payload.__contains__(attr_name)
