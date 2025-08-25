from sqlalchemy_dbtoolkit.orm.session import ORMSessionManager
from sqlalchemy_dbtoolkit.utils.query_operators import get_filter_operator


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

    def select_all_from_table(self, Table, offset=None, limit=None):
        """
        Queries all rows from the specified table, with optional offset and limit.

        Args:
            Table (Base): A SQLAlchemy ORM model/table class.
            offset (int, optional): Number of rows to skip before returning results. Defaults to None.
            limit (int, optional): Maximum number of rows to return. Defaults to None.

        Returns:
            list[Base]: A list of ORM model instances. Empty list if no rows are found.
        """

        with self.session_manager.session_scope(commit=False) as session:
            query = session.query(Table)
            if offset is not None:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)
            result = query.all()
        return result

    def select_one_by_primary_key(self, Table, primary_key):
        """
        Queries a single row from the specified table by its primary key value.

        Args:
            Table (Base): A SQLAlchemy ORM model/table class.
            primary_key (Any): The primary key value to look up.

        Returns:
            Base or None: The ORM model instance if found, otherwise None.
        """

        with self.session_manager.session_scope(commit=False) as session:
            result = session.get(Table, primary_key)
        return result

    def select_one_by_column(self, Table, column_name, column_value, operator_name='eq'):
        """
        Queries a single row from the specified table by a given column value.

        Args:
            Table (Base): A SQLAlchemy ORM model/table class.
            column_name (str): The column name to filter by.
            column_value (Any): The column_value to match in the specified column.
            operator_name (str, optional): The filter operator to use (default 'eq').
                Supported operators: eq, ne, gt, lt, ge, le, like, in, etc.

        Returns:
            Base or None: An instance of the ORM model if found, else None.
        """

        with self.session_manager.session_scope(commit=False) as session:
            column_attr = getattr(Table, column_name, None)
            if column_attr is None:
                raise AttributeError(f"{column_name} is not a valid column of {Table.__name__}")

            operator_func = get_filter_operator(operator_name=operator_name)
            result = session.query(Table).filter(operator_func(column_attr, column_value)).one_or_none()
        return result

    def select_all_by_column(self, Table, column_name, column_value, operator_name='eq'):
        """
        Queries all rows from the specified table by a given column value.

        Args:
            Table (Base): A SQLAlchemy ORM model/table class.
            column_name (str): The column name to filter by.
            column_value (Any): The column_value to match in the specified column.
            operator_name (str, optional): The filter operator to use (default 'eq').
                Supported operators: eq, ne, gt, lt, ge, le, like, in, etc.

        Returns:
            list[Base]: A list of ORM model instances. Empty list if no matches.
        """

        with self.session_manager.session_scope(commit=False) as session:
            column_attr = getattr(Table, column_name, None)
            if column_attr is None:
                raise AttributeError(f"{column_name} is not a valid column of {Table.__name__}")

            operator_func = get_filter_operator(operator_name=operator_name)
            result = session.query(Table).filter(operator_func(column_attr, column_value)).all()

        return result
