from sqlalchemy_dbtoolkit.orm.session import ORMSessionManager


class SelectManager:
    """
    Handles database select operations using SQLAlchemy ORM sessions.
    """

    def __init__(self, engine):
        """
        Initializes the SelectManager with a SQLAlchemy engine.

        Args:
            engine (sqlalchemy.Engine): An initialized SQLAlchemy engine.
        """

        self.session_manager = ORMSessionManager(engine)

    def select_one_by_column(self, Table, column_name, value):
        """
        Queries a single row from the specified table by a given column value.

        Args:
            Table (Base): A SQLAlchemy ORM model/table class.
            column_name (str): The column name to filter by.
            value (Any): The value to match in the specified column.

        Returns:
            Base or None: An instance of the ORM model if found, else None.
        """

        with self.session_manager.session_scope(commit=False) as session:
            query_args = {column_name: value}
            result = session.query(Table).filter_by(**query_args).one_or_none()
        return result
