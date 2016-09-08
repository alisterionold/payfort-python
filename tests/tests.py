import json
from unittest import TestCase

from payfort.cards import Card
from payfort.charges import Charge
from payfort.customer import Customer
from payfort.refunds import Refund
from payfort.tokens import Token
from payfort.errors import RequestError, BankingError, AuthenticationError

API_KEY = "test_sec_k_161b200afc7a9d5443c24"

OPEN_API_KEY = "test_open_k_a7f27acc9510575209a2"

CUSTOMER_DATA = {
    "name": "Test Customer",
    "email": "test@customer.com",
    "description": "Some info"
}

CARD_DATA = {
    "card[name]": "test",
    "card[number]": "4242424242424242",
    "card[exp_month]": "11",
    "card[exp_year]": "2017",
    "card[cvc]": "123"
}

SIMPLE_CARD_DATA = {
    "number": "4242424242424242",
    "exp_month": 11,
    "exp_year": 2016,
    "cvc": "123",
}

CHARGE_DATA = {
    "amount": 1000,
    "currency": "aed",
    "email": "some@example.com",
    "card": "",
    "description": "Two widgets (test@example.com)"
}

INVALID_CARD_DATA = {
    "number": "4000000000000002",
    "exp_month": 11,
    "exp_year": 2016,
    "cvc": "123",
}

REFUND_DATA = {
    "amount": 500,
    "reason": "requested_by_customer"
}


class TestPayFortMixin(TestCase):
    def setUp(self):
        self.customer_id = self.get_response_data(
            self.create_customer()
        ).get("id")
        self.card_id = self.get_response_data(
            self.create_card(self.customer_id)
        ).get("id")

    @staticmethod
    def create_customer():
        return Customer(API_KEY).create(CUSTOMER_DATA)

    @staticmethod
    def create_card(customer_id):
        return Card(API_KEY).create(customer_id, CARD_DATA)

    @staticmethod
    def create_token(card_data):
        token = Token(API_KEY)
        token.auth = (OPEN_API_KEY, "")
        response = token.create(card_data)
        return json.loads(response.text)["id"]

    def create_token_valid_card(self):
        return self.create_token(SIMPLE_CARD_DATA)

    def create_token_invalid_card(self):
        return self.create_token(INVALID_CARD_DATA)

    def create_charge(self):
        CHARGE_DATA.update({"card": self.token})
        return Charge(API_KEY).create(CHARGE_DATA)

    @staticmethod
    def get_response_data(response):
        return json.loads(response.text)


class TestCustomers(TestPayFortMixin):
    def test_creates_customer_without_card(self):
        response = self.create_customer()
        self.assertIn("id", response.text)
        self.assertIn('"name":"Test Customer"', response.text)

    def test_get_customer(self):
        response = Customer(API_KEY).get(self.customer_id)
        self.assertIn(self.customer_id, response.text)

    def test_update_customer(self):
        data = {"name": "Test"}
        response = Customer(API_KEY).update(self.customer_id, data)
        self.assertIn(self.customer_id, response.text)
        self.assertIn('"name":"Test"', response.text)

    def test_get_all_customers(self):
        response = Customer(API_KEY).get_all()
        self.assertEquals(response.status_code, 200)

    def test_create_customer_with_card_token(self):
        customer_data = {
            "email": "new@customer.com",
            "card": self.create_token_valid_card()
        }
        Customer(API_KEY).create(customer_data)


class TestCards(TestPayFortMixin):
    def test_create_card(self):
        response = self.create_card(self.customer_id)
        self.assertIn("id", response.text)
        self.assertIn(self.customer_id, response.text)

    def test_get_card(self):
        response = Card(API_KEY).retrieve(self.customer_id, self.card_id)
        self.assertIn(self.customer_id, response.text)

    def test_get_all_cards(self):
        response = Customer(API_KEY).get_all()
        self.assertEquals(response.status_code, 200)

    def test_delete_card(self):
        Card(API_KEY).delete(self.customer_id, self.card_id)
        with self.assertRaises(RequestError):
            response = Card(API_KEY).retrieve(self.customer_id, self.card_id)
            self.assertEquals(response.status_code, 404)


class TestCharges(TestPayFortMixin):
    def setUp(self):
        self.token = self.create_token_valid_card()
        self.charge_id = self.get_response_data(self.create_charge())["id"]

    def test_create_charge(self):
        self.token = self.create_token_valid_card()
        response = self.create_charge()
        self.assertEquals(response.status_code, 201)
        self.assertIn("id", response.text)
        self.assertIn(self.token, response.text)

    def test_get_charge(self):
        response = Charge(API_KEY).retrieve(self.charge_id)
        self.assertIn(self.charge_id, response.text)
        self.assertEquals(self.get_response_data(response)["state"], "captured")

    def test_get_all_charges(self):
        response = Charge(API_KEY).get_all()
        self.assertEquals(response.status_code, 200)
        self.assertIn(self.charge_id, response.text)


class TestRefunds(TestPayFortMixin):
    def setUp(self):
        self.token = self.create_token_valid_card()
        self.charge_id = self.get_response_data(self.create_charge())["id"]

    def test_create_refund(self):
        REFUND_DATA.update({"charge_id": self.charge_id})
        charge = self.get_response_data(Charge(API_KEY).retrieve(self.charge_id))
        captured_amount = charge["captured_amount"]

        Refund(API_KEY).create(self.charge_id, REFUND_DATA)
        charge = self.get_response_data(Charge(API_KEY).retrieve(self.charge_id))
        captured_amount_after = charge["captured_amount"]
        refunded_amount = charge["refunded_amount"]

        self.assertEquals(
            captured_amount, captured_amount_after + refunded_amount)


class TestErrors(TestPayFortMixin):
    def test_authentication_error(self):
        customer = Customer(API_KEY)
        customer.auth = ("Some invalid token", "")

        with self.assertRaises(AuthenticationError):
            customer.create(CUSTOMER_DATA)

    def test_request_error(self):
        data = {"amount": 1000}
        with self.assertRaises(RequestError):
            Charge(API_KEY).create(data)

    def test_banking_error(self):
        self.token = self.create_token_invalid_card()
        with self.assertRaises(BankingError):
            Charge(API_KEY).create(
                {
                    "amount": 1000,
                    "currency": "aed",
                    "email": "some@example.com",
                    "card": self.token
                }
            )
