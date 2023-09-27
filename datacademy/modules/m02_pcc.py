"""Module containing the logic for module 2."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import load_diabetes

from datacademy.modules.checker import DEFAULT_ADDRESS, DEFAULT_TIMEOUT, DEFAULT_URL

from .module import Module


class Module02(Module):
    """Class for module 2."""

    def __init__(
        self,
        *,
        server_address: str = DEFAULT_ADDRESS,
        server_port: int | None = None,
        server_url: str = DEFAULT_URL,
        timeout: float = DEFAULT_TIMEOUT,
        notebook: bool = True
    ) -> None:
        """Create a new module 2 instance.

        Args:
            server_address (str, optional): Address of the server. Defaults to DEFAULT_ADDRESS.
            server_port (int | None, optional): Port of the server, if a non-default port is used. Defaults to None.
            server_url (str, optional): URL from address[:port] to verification endpoint. Defaults to DEFAULT_URL.
            timeout (float, optional): Seconds before a checking request will time out. Defaults to DEFAULT_TIMEOUT.
            notebook (bool, optional): Whether this checker is run in a notebook. Defaults to True.
        """
        super().__init__(
            'M02_PCC',
            server_address=server_address,
            server_port=server_port,
            server_url=server_url,
            timeout=timeout,
            notebook=notebook
        )

    @staticmethod
    def load_dataset() -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
        """Load the dataset.

        Returns:
            tuple[np.ndarray, np.ndarray, pd.DataFrame]: Tuple of X, Y and the DataFrame.
        """
        data = load_diabetes()
        x: np.ndarray = data['data']  # type: ignore
        y: np.ndarray = data['target']  # type: ignore
        df = pd.DataFrame(x, columns=[
            f'column_{i}' for i in range(x.shape[1])
        ])

        return x, y, df

    @staticmethod
    def display_e6_graph(y: np.ndarray, dataframe: pd.DataFrame) -> None:
        """Display the graph to which the answer of exercise E6 should look similar.

        Args:
            y (np.ndarray): Y.
            dataframe (pd.DataFrame): DataFrame from exercise.
        """
        plt.scatter(y, dataframe['column_1'].to_list(), color='green', label='Column 1')
        plt.scatter(y, dataframe['column_2'].to_list(), color='red', label='Column 2')

        plt.ylim(-0.25, 0.25)

        plt.title('My first plot of column 1 and 2', fontsize=20)
        plt.xlabel('x-axis')
        plt.ylabel('y-axis')

        plt.legend(loc='upper right')
        plt.show()
