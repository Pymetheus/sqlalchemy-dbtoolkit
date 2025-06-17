from sqlalchemy_dbtoolkit.utils.config import Config
from sqlalchemy_dbtoolkit.engine.builder import BaseEngine
from sqlalchemy import text


class PostgreSQLEngine(BaseEngine):
    """
    PostgreSQL-specific implementation of the BaseEngine abstract class.

    Manages engine initialization, configuration loading, and database creation for PostgreSQL databases.
    """

    def __init__(self, db_name, config_path='../../.config/config.ini'):
        """
        Initializes the PostgreSQLEngine with the given database name and config path.

        Args:
            db_name (str): Name of the PostgreSQL database.
            config_path (str): Path to the configuration file. Defaults to '../../.config/config.ini'.
        """

        super().__init__(db_name, config_path)
        self.driver = "psycopg2"
        self.load_config()

    @property
    def dialect(self):
        """
        Returns the SQLAlchemy dialect for PostgreSQL.

        Returns:
            str: Always returns 'postgresql'.
        """
        return "postgresql"

    @property
    def fallback_database(self):
        """
        Provides the fallback database used for administrative operations in PostgreSQL.

        Returns:
            str: The name of the fallback database, 'postgres'.
        """
        return "postgres"

    def load_config(self):
        """
        Loads PostgreSQL configuration from the config file.
        """

        try:
            config = Config(config_path=self.config_path)
            self.username = config.postgresql_user
            self.password = config.postgresql_password
            self.host = config.postgresql_host
            self.port = config.postgresql_port or self.DEFAULT_DB_PORTS.get(self.dialect)
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration: {e}")

    def establish_db_connection(self):
        """
        Checks if the database exists; creates it if necessary, then initializes the engine.
        """

        if not self.database_exists():
            self.create_new_database(self.db_name)
            print("DB CREATED READY TO CONTINUE")
        else:
            print("DB ALREADY EXISTED")
        self.initialize_engine()

    def database_exists(self):
        """
        Checks whether the specified database exists on the PostgreSQL server.

        Returns:
            bool: True if the database exists, False otherwise.
        """

        temp_engine = None
        try:
            temp_engine = self.connect_to_fallback_db()
            with temp_engine.begin() as temp_connection:
                check_db_query = "SELECT datname FROM pg_database WHERE datistemplate = false;"
                result = temp_connection.execute(text(check_db_query))

            for item in result:
                if item[0] == self.db_name:
                    return True
            return False
        except Exception as e:
            raise RuntimeError(f"Failed to check for existing databases: {e}")
        finally:
            if temp_engine:
                temp_engine.dispose()

    def create_new_database(self, new_db):
        """
        Creates a new PostgreSQL database if it does not already exist.

        Args:
            new_db (str): Name of the database to be created.
        """
        temp_engine = None
        try:
            temp_engine = self.connect_to_fallback_db()
            with temp_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as temp_connection:
                create_db_query = f"CREATE DATABASE {new_db}"
                temp_connection.execute(text(create_db_query))
                temp_connection.commit()
        except Exception as e:
            raise RuntimeError(f"Failed to create database {new_db}: {e}")
        finally:
            if temp_engine:
                temp_engine.dispose()
