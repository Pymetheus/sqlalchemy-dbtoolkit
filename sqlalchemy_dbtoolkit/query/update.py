from sqlalchemy_dbtoolkit.orm.session import ORMSessionManager
from sqlalchemy_dbtoolkit.utils.query_operators import get_filter_operator


class UpdateManager:
    """
    Handles database update operations using SQLAlchemy ORM sessions.
    """

    def __init__(self, engine):
        """
        Initializes the UpdateManager with a SQLAlchemy engine.

        Args:
            engine (sqlalchemy.Engine): An initialized SQLAlchemy engine.
        """

        self.session_manager = ORMSessionManager(engine)

    def bulk_update_rows(self, Table, column_name, column_value, update_dict, operator_name='eq'):
        """
        Performs a bulk update on one or more rows in the specified table that match a column value.

        Args:
            Table (Base): A SQLAlchemy ORM model/table class.
            column_name (str): The column name to filter by.
            column_value (Any): The value to match in the specified column.
            update_dict (dict): A dictionary of column-value pairs to update.
            operator_name (str, optional): The filter operator to use (default 'eq').
                Supported operators: eq, ne, gt, lt, ge, le, like, in, etc.

        Returns:
            int: The number of rows updated.
        """

        with self.session_manager.session_scope() as session:
            column_attr = getattr(Table, column_name, None)
            if column_attr is None:
                raise AttributeError(f"{column_name} is not a valid column of {Table.__name__}")

            operator_func = get_filter_operator(operator_name=operator_name)
            updated_rows = session.query(Table).filter(operator_func(column_attr, column_value)).update(update_dict)

        return updated_rows

    def update_rows(self, Table, column_name, column_value, update_dict, operator_name='eq'):
        """
        Updates rows in the specified table that match a column value using ORM objects.

        This method loads the matching rows into memory, updates them one by one,
        and commits the changes. ORM events are fired and the session identity map
        is kept in sync.

        Args:
            Table (Base): A SQLAlchemy ORM model/table class.
            column_name (str): The column name to filter by.
            column_value (Any): The value to match in the specified column.
            update_dict (dict): A dictionary of column-value pairs to update.
            operator_name (str, optional): The filter operator to use (default 'eq').
                Supported operators: eq, ne, gt, lt, ge, le, like, in, etc.

        Returns:
            int: The number of rows updated.
        """
        with self.session_manager.session_scope() as session:
            column_attr = getattr(Table, column_name, None)
            if column_attr is None:
                raise AttributeError(f"{column_name} is not a valid column of {Table.__name__}")

            operator_func = get_filter_operator(operator_name=operator_name)
            matched_rows = session.query(Table).filter(operator_func(column_attr, column_value)).all()

            for row in matched_rows:
                for key, value in update_dict.items():
                    if hasattr(row, key):
                        setattr(row, key, value)
                    else:
                        raise AttributeError(f"{key} is not a valid column of {Table.__name__}")

            return len(matched_rows)
