"""Module containing the core database components."""

import pandas as pd
from sqlalchemy import CursorResult, create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.sql import text


class DatabaseConnection:
    """Class that can be used to establish a new database connection."""

    def __init__(self, database_location: str) -> None:
        """Create a new database connection."""
        self.engine = create_engine(
            f'sqlite:///{database_location}', connect_args={'check_same_thread': False},
        )

    def create_database(self, base: type[DeclarativeBase]) -> None:
        """Create a database.

        NOTE: Drops all existing tables.
        NOTE: For this to work, the relevant models must be imported!

        Args:
            base (type[DeclarativeBase]): Base to use.
        """
        base.metadata.drop_all(bind=self.engine)
        base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """Get a new session.

        Returns:
            Session: Session.
        """
        return Session(bind=self.engine)

    def query(self, sql: str) -> pd.DataFrame | None:
        """Execute an sql query on the database.

        Args:
            sql (str): SQL query.

        Returns:
            pd.DataFrame | None: Dataframe if rows are returned, None otherwise.
        """
        with self.engine.connect() as connection:
            result: CursorResult = connection.execute(text(sql))

            if result.returns_rows:
                columns = list(result.keys())
                data = [list(row) for row in result]

                return pd.DataFrame(columns=columns, data=data)

            if sql.lower().startswith('create'):
                print('Table created successfully!')  # noqa: T201
            elif sql.lower().startswith('insert'):
                print('Data inserted successfully!')  # noqa: T201
            elif sql.lower().startswith('update'):
                print('Data record updated successfully!')  # noqa: T201
            elif sql.lower().startswith('delete'):
                print('Data record deleted successfully!')  # noqa: T201
            elif sql.lower().startswith('drop'):
                print('Table dropped successfully!')  # noqa: T201

            return None


