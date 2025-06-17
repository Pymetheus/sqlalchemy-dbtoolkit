from sqlalchemy_dbtoolkit.orm.session import ORMSessionManager


class InsertManager:
    """
    Handles database insert operations using SQLAlchemy ORM sessions.
    """

    def __init__(self, engine):
        """
        Initializes the InsertManager with a SQLAlchemy engine.

        Args:
            engine (sqlalchemy.Engine): An initialized SQLAlchemy engine.
        """

        self.session_manager = ORMSessionManager(engine)

    def add_row(self, Table, args: dict):
        """
        Inserts a single row into the specified table.

        Args:
            Table (Base): A SQLAlchemy ORM model/table class.
            args (dict): Dictionary of values for the new row.
        """

        with self.session_manager.session_scope() as session:
            row_data = Table(**args)
            session.add(row_data)

    def add_rows(self, Table, args: list[dict]):
        """
        Inserts multiple rows into the specified table.

        Args:
            Table (Base): A SQLAlchemy ORM model/table class.
            args (list[dict]): A list of dictionaries, each representing a new row.
        """

        with self.session_manager.session_scope() as session:
            rows_data = [Table(**arg) for arg in args]
            session.add_all(rows_data)
