import requests

from payfort import api_base

from payfort.payfort import PayFortObject

__all__ = ("Charge",)


class Charge(PayFortObject):
    """
    Charges

    To charge a credit or a debit card, you create a new charge object.
    You can retrieve and refund individual charges as well as list all charges.
    Charges are identified by a unique random ID
    (e.g. ch_913ac1cf34bb962d84f39f729ca4a).
    """
    url = api_base + "/charges"

    def create(self, data):
        """
        Create a new Charge
        This is where the action happens – creating a Charge is how you charge
        a credit / debit card with Start, and it’s really
        easy as you’ll see in a bit.

        HTTP Request

        POST https://api.start.payfort.com/charges/

        """
        return self.handle_response(
            requests.post(self.url, data=data, auth=self.auth)
        )

    def retrieve(self, charge_id):
        """
        Retrieve an existing Charge

        Just pass the unique Charge ID that you got when creating the
        Charge and we’ll send you back the latest details on the charge.

        HTTP Request

        GET https://api.start.payfort.com/charges/{CHARGE_ID}
        """
        return requests.get("%s/%s" % (self.url, charge_id),
                            auth=self.auth)

    def capture(self, charge_id, data):
        """
        Capture a Charge
        This step only applies to Authorizations (i.e. charges originally created with capture=false).

        Uncaptured payments expire exactly seven days after they are created. If they are not captured by that point, then they will be marked as refunded and can no longer be captured.
        HTTP Request

        POST https://api.start.payfort.com/charges/{CHARGE_ID}/capture
        """
        return requests.post(
            "%s/%s/capture" % (self.url, charge_id), data=data,
            auth=self.auth
        )

    def get_all(self):
        """
        List all Charges

        This endpoint retrieves all the charges that you’ve got on your account.
        That’s right .. all of it. The good, the bad and the ugly.
        (The failed and the successful charges).

        The charges are returned in sorted order,
        with the most recent charges appearing first.

        HTTP Request

        GET https://api.start.payfort.com/charges/
        """
        return requests.get(self.url, auth=self.auth)
