"""Module containing the logic for module 3."""

from datetime import datetime

import pandas as pd

from datacademy.checker import DEFAULT_ADDRESS, DEFAULT_TIMEOUT, DEFAULT_URL
from datacademy.database import DatabaseConnection
from datacademy.database.m03 import Base, Customer, Order, Product
from datacademy.modules.module import Module

DEFAULT_DB_LOCATION = 'database.db'

class Module03(Module):
    """Class for module 3."""

    def __init__(
        self,
        *,
        database_location: str = DEFAULT_DB_LOCATION,
        server_address: str = DEFAULT_ADDRESS,
        server_port: int | None = None,
        server_url: str = DEFAULT_URL,
        timeout: float = DEFAULT_TIMEOUT,
        notebook: bool = True
    ) -> None:
        """Create a new module 3 instance.

        Args:
            database_location (str, optional): Address where to save the database. Defaults to DEFAULT_DB_LOCATION.
            server_address (str, optional): Address of the server. Defaults to DEFAULT_ADDRESS.
            server_port (int | None, optional): Port of the server, if a non-default port is used. Defaults to None.
            server_url (str, optional): URL from address[:port] to verification endpoint. Defaults to DEFAULT_URL.
            timeout (float, optional): Seconds before a checking request will time out. Defaults to DEFAULT_TIMEOUT.
            notebook (bool, optional): Whether this checker is run in a notebook. Defaults to True.
        """
        super().__init__(
            'M03_SQL',
            server_address=server_address,
            server_port=server_port,
            server_url=server_url,
            timeout=timeout,
            notebook=notebook
        )

        self.connection = DatabaseConnection(database_location)
        self.connection.create_database(Base)
        self.__init_database()

    def __init_database(self) -> None:
        """Populate the database."""
        with self.connection.get_session() as session:
            # Add customers
            df_customers = pd.read_csv(self.get_resource_path('customers.csv'))
            for _, row in df_customers.iterrows():
                session.add(Customer(row['id'], row['first_name'], row['last_name'], row['address']))

            # Add products
            df_products = pd.read_csv(self.get_resource_path('products.csv'))
            for _, row in df_products.iterrows():
                session.add(Product(row['id'], row['name'], row['price'], row['stock']))

            # Add orders
            df_orders = pd.read_csv(self.get_resource_path('orders.csv'))
            for _, row in df_orders.iterrows():
                date = datetime.strptime(row['date'], '%d/%m/%Y').date()  # noqa: DTZ007
                session.add(Order(row['id'], row['customer_id'], row['product_id'], date, row['quantity']))

            # Commit to DB
            session.commit()

    def query(self, sql: str) -> pd.DataFrame | None:
        """Execute an sql query on the database.

        Args:
            sql (str): SQL query.

        Returns:
            pd.DataFrame | None: Dataframe if rows are returned, None otherwise.
        """
        return self.connection.query(sql)

    def check_query(self, question: str, sql: str) -> None:
        """Check the outcome of a query.

        Args:
            question (str): Question identifier.
            sql (str): SQL query.
        """
        result = self.query(sql)
        if result is not None:
            self.check(question, result)
