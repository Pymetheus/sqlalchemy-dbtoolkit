from sqlalchemy_dbtoolkit.utils.config import Config
from sqlalchemy_dbtoolkit.engine.builder import BaseEngine
import os
from sqlalchemy import URL


class SqliteEngine(BaseEngine):
    """
    SQLite-specific implementation of the BaseEngine abstract class.

    Manages engine initialization and configuration loading for SQLite databases.
    """

    def __init__(self, db_name, config_path='../../.config/config.ini'):
        """
        Initializes the SqliteEngine with the given database name and config path.

        Args:
            db_name (str): Name of the SQLite database (without `.db` extension).
            config_path (str): Path to the configuration file. Defaults to '../../.config/config.ini'.
        """

        super().__init__(db_name, config_path)
        self.sqlite_dir_path = None
        self.load_config()

    @property
    def dialect(self):
        """
        Returns the SQLAlchemy dialect for SQLite.

        Returns:
            str: Always returns 'sqlite'.
        """

        return "sqlite"

    @property
    def fallback_database(self):
        """
        SQLite does not require a fallback database.

        Returns:
            None
        """

        return None

    def load_config(self):
        """
        Loads SQLite configuration from the config file.
        """

        try:
            config = Config(config_path=self.config_path)
            self.sqlite_dir_path = config.sqlite_path
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration: {e}")

    def create_connection_url(self):
        """
        Constructs a SQLAlchemy connection URL for the SQLite database.
        Default SQLite URL string is: 'sqlite:///your_database_name.db'

        Returns:
            sqlalchemy.engine.URL: The SQLite connection URL.
        """

        database_path = os.path.join(self.sqlite_dir_path, f"{self.db_name}.db")
        connection_url = URL.create(
            drivername=self.dialect,
            database=database_path
        )
        return connection_url

    def establish_db_connection(self):
        """
        Initializes the database engine after verifying the target path exists.
        """
        if not os.path.exists(self.sqlite_dir_path):
            raise FileNotFoundError(f"SQLite path '{self.sqlite_dir_path}' does not exist.")

        self.initialize_engine()
        print(f"DB CREATED at: {os.path.join(self.sqlite_dir_path, f'{self.db_name}.db')}")

    def database_exists(self):
        """
        SQLite does not require a separate 'exists' check for databases.
        """
        raise NotImplementedError("Database exists control not required in sqlite")

    def create_new_database(self, new_db):
        """
        SQLite automatically creates databases upon connection.
        """
        raise NotImplementedError("Create new database not required in sqlite")
