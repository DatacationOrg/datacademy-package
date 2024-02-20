"""Module containing the logic for module 10."""

import pandas as pd

from datacademy.checker import DEFAULT_ADDRESS, DEFAULT_TIMEOUT, DEFAULT_URL

from .module import Module


class Module07(Module):
    """Class for module 07."""

    def __init__(
        self,
        *,
        server_address: str = DEFAULT_ADDRESS,
        server_port: int | None = None,
        server_url: str = DEFAULT_URL,
        timeout: float = DEFAULT_TIMEOUT,
        notebook: bool = True
    ) -> None:
        """Create a new module 07 instance.

        Args:
            server_address (str, optional): Address of the server. Defaults to DEFAULT_ADDRESS.
            server_port (int | None, optional): Port of the server, if a non-default port is used. Defaults to None.
            server_url (str, optional): URL from address[:port] to verification endpoint. Defaults to DEFAULT_URL.
            timeout (float, optional): Seconds before a checking request will time out. Defaults to DEFAULT_TIMEOUT.
            notebook (bool, optional): Whether this checker is run in a notebook. Defaults to True.
        """
        super().__init__(
            'M07_FINAL',
            server_address=server_address,
            server_port=server_port,
            server_url=server_url,
            timeout=timeout,
            notebook=notebook
        )


    def check_df(self, question: str, df: pd.DataFrame) -> None:
        """Check the outcome of a query.

        Args:
            question (str): Question identifier.
            df (pd.DataFrame): DataFrame containing the answer.
        """
        self.check(question, df)
