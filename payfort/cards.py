import requests

from payfort import api_base

from payfort.payfort import PayFortObject

__all__ = ("Card",)


class Card(PayFortObject):
    """
    When you create a new Card, you must specify a Customer to create it on.
    If the customer has no default card, then the new card will
    become the default.
    However, if the customer already has a default then it will not change.
    To change the default, you should update the customer and pass the new
    default_card_id.
    """
    url = api_base + "/customers"

    def create(self, customer_id, data):
        """
        Create a Card
        HTTP Request
        POST https://api.start.payfort.com/customers/{CUSTOMER_ID}/cards
        """
        return self.handle_response(requests.post(
            "%s/%s/cards" % (self.url, customer_id), data=data,
            auth=self.auth
        ))

    def retrieve(self, customer_id, card_id):
        """
        Retrieve a Card

        Just pass the unique card ID that you got when creating the Card
        and we’ll send you back the latest details on the card.

        HTTP Request

        GET https://api.start.payfort.com/customers/{CUSTOMER_ID}/cards/{CARD_ID}

        """
        return self.handle_response(requests.get(
            "%s/%s/cards/%s" % (self.url, customer_id, card_id),
            auth=self.auth
        ))

    def delete(self, customer_id, card_id):
        """
        Delete a Card

        This action permanently deletes a card.
        Previous transactions made using this card are not affected.

        HTTP Request

        DELETE https://api.start.payfort.com/customers/{CUSTOMER_ID}/cards/{CARD_ID}

        """
        return self.handle_response(requests.delete(
            "%s/%s/cards/%s" % (self.url, customer_id, card_id),
            auth=self.auth
        ))

    def get_all(self, customer_id):
        """
        List all Cards

        This endpoint returns a list of all of the cards for
        the specified customer.
        The cards are returned in sorted order, with the most recent cards
        appearing first.
        HTTP Request

        GET https://api.start.payfort.com/customers/{CUSTOMER_ID}/cards
        """
        return self.handle_response(requests.get(
            "%s/%s/cards" % (self.url, customer_id), auth=self.auth
        ))
