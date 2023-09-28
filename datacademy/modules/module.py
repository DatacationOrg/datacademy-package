"""Module containing the module base class."""
from pathlib import Path

from datacademy.checker.checker import DEFAULT_ADDRESS, DEFAULT_TIMEOUT, DEFAULT_URL, Checker, T


class Module:
    """Base class for a module."""

    RESOURCE_FOLDER = 'resources'

    def __init__(
        self,
        name: str,
        *,
        server_address: str = DEFAULT_ADDRESS,
        server_port: int | None = None,
        server_url: str = DEFAULT_URL,
        timeout: float = DEFAULT_TIMEOUT,
        notebook: bool = True
    ) -> None:
        """Create a new module.

        Args:
            name (str):
                Module name.
            server_address (str, optional):
                Address of the server. Defaults to DEFAULT_ADDRESS.
            server_port (int | None, optional):
                Port of the server, if a non-default port is used. Defaults to None.
            server_url (str, optional):
                URL from address[:port] to verification endpoint. Defaults to DEFAULT_URL.
            timeout (float, optional):
                Seconds before a checking request will time out. Defaults to DEFAULT_TIMEOUT.
            notebook (bool, optional):
                Whether this checker is run in a notebook. Defaults to True.
        """
        self.name = name
        self.checker = Checker(
            name,
            server_address=server_address,
            server_port=server_port,
            server_url=server_url,
            timeout=timeout,
            notebook=notebook
        )

    def check(self, question: str, answer: T) -> None:
        """Check an answer.

        Args:
            question (str): Question identifier.
            answer (T): The answer.
        """
        self.checker.check(question, answer)

    def get_resource_path(self, *path: str | Path) -> Path:
        """Get the path to a resource.

        Returns:
            Path: Path within resource folder.
        """
        return Path(self.RESOURCE_FOLDER, *path)
