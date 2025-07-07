from sqlalchemy import inspect


class InspectionManager:
    """
    Utility class for inspecting database schema metadata using SQLAlchemy's inspection system.
    """

    def __init__(self, engine):
        """
        Initializes the InspectionManager with a given SQLAlchemy engine.

        Args:
            engine (sqlalchemy.engine.Engine): SQLAlchemy engine instance connected to the database.
        """

        self.inspector = inspect(engine)

    def has_table(self, table_name, schema=None):
        """
        Checks if a table exists within the given schema.

        Args:
            table_name (str): Name of the table to check.
            schema (str, optional): Target schema to search within. Defaults to the default schema.

        Returns:
            bool: True if the table exists, False otherwise.
        """

        return self.inspector.has_table(table_name, schema=schema)

    def get_table_names(self, schema=None):
        """
        Retrieves a list of all table names in the specified schema.

        Args:
            schema (str, optional): Schema name to search within. Defaults to the default schema.

        Returns:
            list[str]: List of table names found in the schema.
        """

        return self.inspector.get_table_names(schema=schema)

    def get_schema_names(self):
        """
        Retrieves a list of all schemas available in the database.

        Returns:
            list[str]: List of schema names present in the database.
        """

        return self.inspector.get_schema_names()

    def get_columns(self, table_name, schema=None):
        """
        Retrieves the column definitions for a specified table.

        Args:
            table_name (str): Name of the table to inspect.
            schema (str, optional): Schema containing the table. Defaults to the default schema.

        Raises:
            ValueError: If the specified table does not exist in the schema.

        Returns:
            list[dict]: A list of dictionaries describing the table's columns.
        """

        if not self.has_table(table_name, schema=schema):
            raise ValueError(f"Table '{table_name}' does not exist in schema '{schema}'.")

        return self.inspector.get_columns(table_name, schema=schema)

    def get_foreign_keys(self, table_name, schema=None):
        """
        Retrieves foreign key constraints for the specified table.

        Args:
            table_name (str): Name of the table to inspect.
            schema (str, optional): Schema containing the table. Defaults to the default schema.

        Raises:
            ValueError: If the specified table does not exist in the schema.

        Returns:
            list[dict]: A list of foreign key constraint definitions.
        """

        if not self.has_table(table_name, schema=schema):
            raise ValueError(f"Table '{table_name}' does not exist in schema '{schema}'.")

        return self.inspector.get_foreign_keys(table_name, schema=schema)

    def get_primary_key_constraint(self, table_name, schema=None):
        """
        Retrieves the primary key constraint information for the specified table.

        Args:
            table_name (str): Name of the table to inspect.
            schema (str, optional): Schema containing the table. Defaults to the default schema.

        Raises:
            ValueError: If the specified table does not exist in the schema.

        Returns:
            dict: A dictionary describing the primary key constraint.
        """

        if not self.has_table(table_name, schema=schema):
            raise ValueError(f"Table '{table_name}' does not exist in schema '{schema}'.")

        return self.inspector.get_pk_constraint(table_name, schema=schema)

