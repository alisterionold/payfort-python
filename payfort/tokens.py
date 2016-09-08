import requests
from payfort.payfort import PayFortObject

from payfort import api_base

__all__ = ("Token",)


class Token(PayFortObject):
    """
    You don’t want sensitive card information ending up on your servers.
    Therefore, it’s best to replace them (immediately) with a token.
    You do this by sending the Card details directly from the customers
     browser to our API .. so that the card details never touch your server.

    You can easily do this using our start.js library.

    Tokens are created with your open
    API key (yours is test_open_k_9091f35e42fe3cfc2ac9),
    which can safely be included in your client side source code,
    or in downloadable applications like iPhone/Android apps.
    Note that tokens should not be stored or used more than once —
    to store these details for use later, you should immediately
    create a Customer) from the token you get back.
    The Customer ID can then be stored and charged at
    a later time / multiple times.
    """

    url = api_base + '/tokens'

    def create(self, data):
        """
        Create a new Token
        You can create a token by making the following request:

        HTTP Request

        POST https://api.start.payfort.com/tokens/
        """
        return self.handle_response(
            requests.post(self.url, data=data, auth=self.auth, )
        )
