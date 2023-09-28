"""Module containing the logic for module 5."""

import json

from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import Response

from datacademy.checker import DEFAULT_ADDRESS, DEFAULT_TIMEOUT, DEFAULT_URL

from .module import Module


class Module05(Module):
    """Class for module 5."""

    def __init__(
        self,
        app: FastAPI | None = None,
        *,
        server_address: str = DEFAULT_ADDRESS,
        server_port: int | None = None,
        server_url: str = DEFAULT_URL,
        timeout: float = DEFAULT_TIMEOUT,
        notebook: bool = True
    ) -> None:
        """Create a new module 5 instance.

        Args:
            app (FastAPI| None, optional): Reference to the FastAPI app. Defaults to None.
            server_address (str, optional): Address of the server. Defaults to DEFAULT_ADDRESS.
            server_port (int | None, optional): Port of the server, if a non-default port is used. Defaults to None.
            server_url (str, optional): URL from address[:port] to verification endpoint. Defaults to DEFAULT_URL.
            timeout (float, optional): Seconds before a checking request will time out. Defaults to DEFAULT_TIMEOUT.
            notebook (bool, optional): Whether this checker is run in a notebook. Defaults to True.
        """
        super().__init__(
            'M05_API',
            server_address=server_address,
            server_port=server_port,
            server_url=server_url,
            timeout=timeout,
            notebook=notebook
        )
        if app:
            self.client = TestClient(app)

    def load_customers(self) -> dict[int, dict[str, str]]:
        """Load the customer data.

        Returns:
            dict[int, dict[str, str]]: Dictionary of customer id to customer.
        """
        with self.get_resource_path('customers.json').open() as file:
            return dict(enumerate(json.load(file)))

    def __check_status(self, response: Response, url: str) -> Response:
        if response.status_code != 200:  # noqa: PLR2004
            raise ValueError(f'Expected response code 200 for {url}, but got {response.status_code} instead.')

        return response

    def check_get(self, question: str, url: str) -> None:
        """Check a GET request.

        Args:
            question (str): Question ID.
            url (str): URL to get.
        """
        response: Response = self.__check_status(self.client.get(url), url)
        self.check(question, response.json())


# def test_get_customers():
#     response = client.get('/get-customers/')
#     assert response.status_code == 200
#     assert response.json() == {
#         '0': {
#             'firstName': 'John',
#             'lastName': 'Doe',
#             'address': '1948 Conifer Drive'
#             },
#         '1': {
#             'firstName': 'Arthur',
#             'lastName': 'Holmes',
#             'address': '2149 Stockert Hollow Road'
#             },
#         '2': {
#             'firstName': 'Jamie',
#             'lastName': 'Dean',
#             'address': '4883 White Lane'
#             }
#         }


# def test_create_customer():
#     data = {
#         'firstName': 'Jan',
#         'lastName': 'Janssen',
#         'address': 'Kerkstraat 10'
#            }

#     response = client.post('/create-customer/12?firstName=Jan&lastName=Janssen&address=Kerkstraat%2010')

#     assert response.status_code == 200
#     assert response.json() == data


# def test_create_customer_auto_increment():
#     response = client.get('/get-customers/?skip=0&limit=1000')
#     keys_customers = list(response.json().keys())

#     assert response.status_code == 200
#     assert (int(keys_customers[-1]) - int(keys_customers[-2])) == 1


# def test_update_customer_address():
#     data = {'address': 'Ons Dorp 100'}

#     response = client.put('/update-customer-address/1?address=Ons%20Dorp%20100')
#     assert response.status_code == 200
#     assert response.json()['address'] == data['address']
#     assert client.get('/get-customer/1').json()['address'] == data['address']


# def test_update_customer_address_by_name():
#     data = {
#         'firstName': 'John',
#         'lastName': 'Doe',
#         'address': 'Imaginary street 1'
#         }

#     response = client.put('/update-customer-address-by-name/?firstName=John&lastName=Doe&address=Imaginary%20street%201')

#     assert response.status_code == 200
#     assert response.json()['address'] == data['address']
#     assert client.get(
#         '/get-customer/0').json()['address'] == data['address']


# def test_delete_customer():
#     response = client.delete('/delete-customer/0')

#     assert response.status_code == 200
#     assert response.json() == {'Message': 'Customer 0 deleted successfully.'}
#     assert 'Customer does not exists yet.' in client.get('/get-customer/0').json()


# def test_delete_customer_by_name():
#     response = client.delete('/delete-customer-by-name/?firstName=Jamie&lastName=Dean')

#     assert response.status_code == 200
#     assert response.json() == {'Message': 'Customer Jamie Dean deleted successfully.'}
#     assert 'Customer does not exists yet.' in client.get('/get-customer/2').json()
