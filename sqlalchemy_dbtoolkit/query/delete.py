from sqlalchemy_dbtoolkit.orm.session import ORMSessionManager
from sqlalchemy_dbtoolkit.utils.query_operators import get_filter_operator


class DeleteManager:
    """
    Handles database delete operations using SQLAlchemy ORM sessions.
    """

    def __init__(self, engine):
        """
        Initializes the DeleteManager with a SQLAlchemy engine.

        Args:
            engine (sqlalchemy.Engine): An initialized SQLAlchemy engine.
        """

        self.session_manager = ORMSessionManager(engine)

    def delete_row(self, row_instance):
        """
        Deletes a single ORM object from the database.

        Args:
            row_instance (Base): An instance of a SQLAlchemy ORM model to delete.

        Returns:
            One
        """

        if row_instance is None:
            raise ValueError("Cannot delete a None object")

        with self.session_manager.session_scope() as session:
            session.delete(row_instance)

        return 1

    def delete_rows(self, row_instances):
        """
        Deletes multiple ORM objects at once.

        Args:
            row_instances (list[Base]): A list of SQLAlchemy ORM model instances to delete.

        Returns:
            int: The number of rows deleted.
        """

        if row_instances is None:
            raise ValueError("Must be a non-empty list of ORM objects")

        with self.session_manager.session_scope() as session:
            for instance in row_instances:
                session.delete(instance)

        return len(row_instances)

    def delete_rows_by_filter(self, Table, column_name, column_value, operator_name='eq'):
        """
            Deletes rows from the specified table based on a filter condition.

            Args:
                Table (Base): A SQLAlchemy ORM model/table class.
                column_name (str): The column name to filter by.
                column_value (Any): The value to match in the specified column.
                operator_name (str, optional): The filter operator to use (default 'eq').
                    Supported operators: eq, ne, gt, lt, ge, le, like, in, etc.

            Returns:
                int: The number of rows deleted.
            """

        with self.session_manager.session_scope() as session:
            column_attr = getattr(Table, column_name, None)
            if column_attr is None:
                raise AttributeError(f"{column_name} is not a valid column of {Table.__name__}")

            operator_func = get_filter_operator(operator_name=operator_name)
            deleted_rows = session.query(Table).filter(operator_func(column_attr, column_value)).delete(
                synchronize_session=False)

        return deleted_rows
