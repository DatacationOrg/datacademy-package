"""Module containing the logic for module 4."""

import random

import numpy as np
import pandas as pd
from sklearn import datasets

from datacademy.checker import DEFAULT_ADDRESS, DEFAULT_TIMEOUT, DEFAULT_URL

from .module import Module


class Module04(Module):
    """Class for module 4."""

    def __init__(
        self,
        *,
        server_address: str = DEFAULT_ADDRESS,
        server_port: int | None = None,
        server_url: str = DEFAULT_URL,
        timeout: float = DEFAULT_TIMEOUT,
        notebook: bool = True
    ) -> None:
        """Create a new module 4 instance.

        Args:
            server_address (str, optional): Address of the server. Defaults to DEFAULT_ADDRESS.
            server_port (int | None, optional): Port of the server, if a non-default port is used. Defaults to None.
            server_url (str, optional): URL from address[:port] to verification endpoint. Defaults to DEFAULT_URL.
            timeout (float, optional): Seconds before a checking request will time out. Defaults to DEFAULT_TIMEOUT.
            notebook (bool, optional): Whether this checker is run in a notebook. Defaults to True.
        """
        super().__init__(
            'M04_ML',
            server_address=server_address,
            server_port=server_port,
            server_url=server_url,
            timeout=timeout,
            notebook=notebook
        )

        # Set random seeds
        random.seed(41)
        np.random.seed(41)

        # Set imputed outlier index
        self.imputed_outlier_index = 72

        # Load data
        self.data: dict[str, np.ndarray | list] = datasets.load_iris() # type: ignore

        # Initialize unsupervised dataset variable
        self._unsupervised: pd.DataFrame | None = None

    def load_dataset(self) -> pd.DataFrame:
        """Load the dataset.

        Returns:
            pd.DataFrame: Dataset.
        """
        df = pd.DataFrame(data=self.data['data'], columns=self.data['feature_names'])

        # Create NaN values (missing values) in petal width
        none_values = [random.randint(0, 149) for _ in range(5)]  # noqa: S311
        df.loc[none_values, 'petal length (cm)'] = None

        # Transform one column its measure unit
        df = df.rename(columns={'sepal width (cm)': 'sepal width (mm)'})
        df['sepal width (mm)'] = df['sepal width (mm)'].apply(lambda x: x * 10)

        # Add outlier to the DataFrame
        index_val = self.imputed_outlier_index
        value = df.loc[index_val, 'sepal length (cm)']
        new_value = float(str(value).split('.')[0] + '0.' + str(value).split('.')[-1])
        df.loc[index_val, 'sepal length (cm)'] = new_value

        return df

    def add_state(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add a column for numerical features.

        Args:
            df (pd.DataFrame): DataFrame.

        Returns:
            pd.DataFrame: Updated DataFrame.
        """
        df['state'] = np.random.choice(['wet', 'dry'], df.shape[0])
        return df


    def remove_zero_in_outlier(self, df: pd.DataFrame, outlier_value: float) -> None:
        """Modify the outlier by removing the first zero.

        Args:
            df (pd.DataFrame): Dataframe.
            outlier_value (float): Outlier value.
        """
        # Get outlier index
        outlier_idx = df[df['sepal length (cm)'] == outlier_value].index[0]

        # Get index of first occurrence of '0'
        zero_idx = str(outlier_value).index('0')

        # Remove the first occurrence of '0'
        new_value = float(str(outlier_value)[:zero_idx] + str(outlier_value)[zero_idx + 1:])

        # Append the new value to the DataFrame
        df.loc[outlier_idx, 'sepal length (cm)'] = new_value

    def get_supervised(self) -> pd.DataFrame:
        """Prepare the dataset for supervised learning.

        Args:
            df (pd.DataFrame): Dataset.
        """
        df = self.load_dataset()
        df = self.add_state(df)
        df['target'] = self.data['target']
        return df
