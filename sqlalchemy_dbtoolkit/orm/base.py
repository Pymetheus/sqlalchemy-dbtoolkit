from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData
from sqlalchemy_dbtoolkit.core.inspector import InspectionManager
Base = declarative_base()


class ORMBaseManager:
    """
    Manager class for handling SQLAlchemy ORM table operations
    using the provided SQLAlchemy engine and declarative base.
    """

    def __init__(self, engine, base=Base, schema=None):
        """
        Initializes the ORMBaseManager with a given SQLAlchemy engine,
        declarative base, and optional schema.

        Args:
            engine (sqlalchemy.engine.Engine): SQLAlchemy engine instance.
            base (sqlalchemy.orm.DeclarativeMeta): Declarative base used for ORM mappings.
            schema (str, optional): Database schema to target.
        """

        self.engine = engine
        self.Base = base
        self.schema = schema
        self.inspector = InspectionManager(self.engine)

    def is_existing_metadata_table(self, table_name):
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

    def create_tables_if_not_exists(self):
        """
        Creates any ORM-defined tables that do not yet exist in the connected database.

        Compares the tables defined in the SQLAlchemy metadata with those
        present in the target database. If all metadata tables are missing,
        they are created using the full metadata. If only some are missing,
        only the missing tables are created using a temporary metadata object.
        """

        metadata_set = set(self.get_metadata_tables())
        database_set = set(self.inspector.get_table_names(schema=self.schema))
        missing_tables = metadata_set - database_set

        if not missing_tables:
            print("TABLES ALREADY EXISTED")
        elif missing_tables == metadata_set:
            self.create_tables()
        else:
            print(f"MISSING TABLES: {missing_tables}")
            missing_metadata = MetaData()
            for table_name in missing_tables:
                table = self.Base.metadata.tables[table_name]
                table.tometadata(missing_metadata, schema=self.schema)
            missing_metadata.create_all(bind=self.engine)

    def drop_all_metadata_tables(self):
        """
        Drops all tables associated with the ORM's metadata using the provided engine.
        """
        self.Base.metadata.drop_all(bind=self.engine)

    def get_metadata_tables(self):
        """
        Retrieves a list of all table names defined in the ORM metadata.

        Returns:
            list[str]: A list of table names.
        """
        return list(self.Base.metadata.tables.keys())
