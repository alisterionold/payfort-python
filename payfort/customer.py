import requests
from payfort.payfort import PayFortObject

from payfort import api_base

__all__ = ("Customer",)


class Customer(PayFortObject):
    URL = api_base + "/customers"

    def create(self, data):
        return self.handle_response(
            requests.post(self.URL, data=data, auth=self.auth))

    def get(self, customer_id):
        return self.handle_response(
            requests.get("%s/%s" % (self.URL, customer_id), auth=self.auth))

    def update(self, customer_id, data):
        return self.handle_response(
            requests.put("%s/%s" % (self.URL, customer_id),
                         data=data,
                         auth=self.auth))

    def delete(self, customer_id):  # Currently unavailable
        return self.handle_response(requests.delete(
            "%s/%s" % (self.URL, customer_id), auth=self.auth))

    def get_all(self):
        return self.handle_response(requests.get(self.URL, auth=self.auth))
