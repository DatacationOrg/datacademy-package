"""Module containing the checker class."""

import json
from collections.abc import Collection
from datetime import datetime
from typing import TypeVar

import pandas as pd
import requests
from IPython.display import display
from requests import Response

from datacademy.util.animation import TextAnimation

from .request import VerificationRequest
from .response import VerificationMessage, VerificationResponse

T = TypeVar('T', float, int, datetime, str, list, dict, pd.DataFrame)
"""Type variable for supported data types to send."""

DEFAULT_ADDRESS = 'localhost'
"""Address where the Datacademy API is hosted."""

DEFAULT_URL = '/verify'
"""URL at address where verification requests should be sent."""

DEFAULT_TIMEOUT = 30.0
"""Seconds before checking request will time out."""

ERROR = '🔴 ERROR:'
"""Start of error message."""


class Checker:
    """Class that can be used at the Datacademy user to check the answers."""

    def __init__(
        self,
        module: str,
        *,
        server_address: str = DEFAULT_ADDRESS,
        server_port: int | None = None,
        server_url: str = DEFAULT_URL,
        timeout: float = DEFAULT_TIMEOUT,
        notebook: bool = True
    ) -> None:
        """Create a new Checker.

        Args:
            module (str): Identifier of the module. Defaults to None.
            server_address (str, optional): Address of the server. Defaults to DEFAULT_ADDRESS.
            server_port (int | None, optional): Port of the server, if a non-default port is used. Defaults to None.
            server_url (str, optional): URL from address[:port] to verification endpoint. Defaults to DEFAULT_URL.
            timeout (float, optional): Seconds before a checking request will time out. Defaults to DEFAULT_TIMEOUT.
            notebook (bool, optional): Whether this checker is run in a notebook. Defaults to True.
        """
        self.module = module
        self.notebook = notebook
        self.timeout = timeout

        try:
            response = requests.get('https://proddatacademyapi.azurewebsites.net/', timeout=60)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            # If the request was successful, store the URL in a variable
            server_address = 'https://proddatacademyapi.azurewebsites.net'
        except requests.exceptions.RequestException as e:
            print(f'Error accessing server: {e}')

        if server_address == 'localhost':
            server_address = 'http://127.0.0.1'
        elif not server_address.startswith('https://'):
            server_address = 'https://' + server_address

        self.url = server_address + ('' if server_port is None else f':{server_port}') + server_url

    def check(
        self,
        question: str,
        answer: T,
    ) -> None:
        """Check an answer.

        Args:
            question (str): Question identifier.
            answer (T): The answer.

        Raises:
            TypeError: If a non-JSON related type error occurs.
        """
        try:
            response = self.__request_verification(question, answer)
        except TimeoutError:
            self.__print_error('Checking the answer timed out.')
            return
        except NotImplementedError:
            self.__print_error(f'Answer of type {type(answer)} is not supported!')
            return
        except TypeError as error:
            if 'JSON' in str(error):
                self.__print_error(f'Answer cannot be converted to JSON: {error!s}')
                return
            raise

        self.__process_response(response)

        if self.notebook:
            display(answer)
        else:
            print(answer)

    def __print_error(self, message: str) -> None:
        """Print error.

        Args:
            message (str): Error message.
        """
        print(ERROR, message)

    def __request_verification(self, question: str, answer: T) -> Response:
        """Request verfication from the API server.

        Args:
            question (str): Question identifier.
            answer (T): Answer.

        Returns:
            Response: Response to request.
        """
        data = VerificationRequest.create(module=self.module, question=question, answer=answer).model_dump_json()
        headers = {
            'Content-Type': 'application/json'
        }

        def _animation(step: int) -> str:
            return '🔵 Checking your answer' + '.' * (step % 4)

        animation = TextAnimation(_animation, frequency=4)
        try:
            animation.start()
            response = requests.request('POST', self.url, headers=headers, data=data, timeout=30)
        finally:
            animation.stop()

        return response

    def __process_response(self, response: Response) -> None:
        """Handle the verification response.

        Args:
            response (Response): Verification response.
        """
        # Print any error that may occur
        if response.status_code != 200:  # noqa: PLR2004
            try:
                message = json.loads(response.content)['detail']
                self.__print_error(f'Server returned {response.status_code} - {message}')
            except BaseException:  # noqa: BLE001
                self.__print_error(f'Server returned {response.status_code}')
            return

        # Load answer and show if correct
        answer_response = VerificationResponse(**json.loads(response.content))
        if answer_response.correct:
            print('🟢 ' + answer_response.message_correct)
        else:
            print('🟠 ' + answer_response.message_incorrect)

        # Print errors
        if len(answer_response.errors) > 0:
            self.__print_messages(answer_response.errors)

        # Print hints
        if len(answer_response.hints) > 0:
            print('🟣 ' + answer_response.message_hints)
            self.__print_messages(answer_response.hints)

        # Print information
        if len(answer_response.info) > 0:
            print('🔵 ' + answer_response.message_info)
            self.__print_messages(answer_response.info)

    def __print_messages(self, messages: Collection[VerificationMessage], indent: str = '  ') -> None:
        """Nicely print messages to the output.

        Args:
            messages (Collection[Message]): Messages.
            indent (str, optional): Single indent to use. Defaults to '  '.
        """
        for message in messages:
            print(indent, '-', message.message)
            if message.obj is None:
                continue

            obj = message.obj.get()
            if isinstance(obj, pd.DataFrame):
                if self.notebook:
                    display(obj)
                else:
                    print(obj)
            elif isinstance(obj, list):
                for item in obj:
                    print(indent * 2, '-', item)
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    print(indent * 2, '-', key, ':', value)
            else:
                print(message.obj)
