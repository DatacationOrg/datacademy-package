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
            url (str): URL to use.
        """
        response: Response = self.__check_status(self.client.get(url), url)
        self.check(question, response.json())

    def check_post(self, question:str, post_url: str, get_url: str) -> None:
        """Check a POST request.

        Args:
            question (str): Question ID.
            post_url (str): POST URL to use.
            get_url (str): GET URL to use.
        """
        self.__check_status(self.client.post(post_url), post_url)
        self.check_get(question, get_url)

    def check_put(self, question:str, put_url: str, get_url: str) -> None:
            """Check a PUT request.

            Args:
                question (str): Question ID.
                put_url (str): POST URL to use.
                get_url (str): GET URL to use.
            """
            self.__check_status(self.client.put(put_url), put_url)
            self.check_get(question, get_url)

    def check_delete(self, question:str, delete_url: str, get_url: str) -> None:
            """Check a PUT request.

            Args:
                question (str): Question ID.
                delete_url (str): POST URL to use.
                get_url (str): GET URL to use.
            """
            self.__check_status(self.client.delete(delete_url), delete_url)
            self.check_get(question, get_url)
