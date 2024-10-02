import logging
import traceback

from utils.exceptions import NotFoundException, ValidationException

from .utils import get_json_response, getInfoFromPartial

logger = logging.getLogger(__name__)


def handle_failure_api(function):
    """
    A decorator to handle failure and return failure json response
    """
    def wrapper(request, *args, **kwargs):
        status = 200
        try:
            return function(request, *args, **kwargs)
        except NotFoundException as e:
            status = 404
            message = str(e)
            logger.error(
                f"Error in ajax {getInfoFromPartial(function)} : {traceback.format_exc()}")
        except ValidationException as e:
            status = 400
            message = str(e)
            logger.error(
                f"Error in ajax {getInfoFromPartial(function)} : {traceback.format_exc()}")
        except Exception as e:
            logger.error(
                f"Error in ajax {getInfoFromPartial(function)} : {traceback.format_exc()}")
            message = str(e)
            status = 500
        return get_json_response(message, status)

    return wrapper
