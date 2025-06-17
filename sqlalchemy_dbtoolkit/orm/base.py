from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ORMBaseManager:
    """
    Manager class for handling SQLAlchemy ORM table operations
    using the provided SQLAlchemy engine and declarative base.
    """

    def __init__(self, engine, base=Base):
        """
        Initializes the ORMBaseManager with a given SQLAlchemy engine and base class.

        Args:
            engine (sqlalchemy.engine.Engine): SQLAlchemy engine instance.
            base (sqlalchemy.orm.DeclarativeMeta): Declarative base used for ORM mappings.
        """

        self.engine = engine
        self.Base = base

    def is_existing_table(self, table_name):
        """
        Checks if a table is already registered in the SQLAlchemy metadata.

        Args:
            table_name (str): Name of the table to check.

        Returns:
            bool: True if the table exists in the metadata, False otherwise.
        """

        return table_name in self.Base.metadata.tables

    def create_tables(self):
        """
        Creates all tables defined in the ORM's metadata using the provided engine.
        """

        self.Base.metadata.create_all(bind=self.engine)

    def drop_all_tables(self):
        """
        Drops all tables associated with the ORM's metadata using the provided engine.
        """
        self.Base.metadata.drop_all(bind=self.engine)

    def get_tables(self):
        """
        Retrieves a list of all table names defined in the ORM metadata.

        Returns:
            list[str]: A list of table names.
        """
        return list(self.Base.metadata.tables.keys())
