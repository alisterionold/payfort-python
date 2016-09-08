__all__ = (
    "PayFortError",
    "SSLError",
    "AuthenticationError",
    "BankingError",
    "ProcessingError",
    "RequestError"
)


class PayFortError(Exception):
    def __init__(self, message="Unknown error", http_status="", error_code="",
                 extras=None):
        self.message = message
        self.http_status = http_status
        self.error_code = error_code
        self.extras = extras if extras else {}

    def __str__(self):
        return self.message + " (" + str(self.extras) + ") "


class SSLError(Exception):
    pass


class AuthenticationError(PayFortError):
    type = "authentication"


class BankingError(PayFortError):
    type = "banking"


class ProcessingError(PayFortError):
    type = "processing"


class RequestError(PayFortError):
    type = "request"


ERROR_TYPES = {
    "authentication": AuthenticationError,
    "banking": BankingError,
    "processing": ProcessingError,
    "request": RequestError
}
