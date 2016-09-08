import json
from payfort.errors import ERROR_TYPES, PayFortError

__all__ = ("PayFortObject",)


class PayFortObject(object):
    def __init__(self, key):
        self.auth = (key, '')

    @staticmethod
    def _parse_errors(response):
        try:
            json_error = json.loads(response.text).get("error", {})
        except (ValueError, TypeError):
            json_error = {}

        return json_error.get("type"), json_error.get(
            "message"), json_error.get("extras")

    def handle_response(self, response):
        if response.status_code in range(200, 300):
            return response

        error_type, message, extras = self._parse_errors(response)
        if not error_type:
            raise PayFortError(response.content)

        raise ERROR_TYPES[error_type](message=message, extras=extras)
