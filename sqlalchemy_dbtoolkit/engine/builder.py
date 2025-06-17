import re
from sqlalchemy import URL, create_engine
from abc import ABC, abstractmethod


class BaseEngine(ABC):
    """
    Abstract base class for SQLAlchemy database engines.
    Provides structure for implementing connection logic, config loading,
    and database creation across various DBMS types.
    """

    DEFAULT_DB_PORTS = {
        "mariadb": 3306,
        "mssql": 1433,
        "mysql": 3306,
        "oracle": 1521,
        "postgresql": 5432
    }

    def __init__(self, db_name, config_path='../../.config/config.ini'):
        """
        Initialize the base engine with a sanitized database name and config path.

        Args:
            db_name (str): Name of the target database.
            config_path (str): Path to the configuration file. Defaults to '../../.config/config.ini'
        """

        self.sanitize_db_name(db_name)
        self.db_name = db_name
        self.config_path = config_path
        self.driver = None
        self.username = None
        self.password = None
        self.host = None
        self.port = None
        self.engine = None

    @property
    @abstractmethod
    def dialect(self):
        """
        Return the SQLAlchemy dialect string for the specific DBMS.
        """
        pass

    @property
    @abstractmethod
    def fallback_database(self):
        """
        Return the fallback database name used to connect when target DB may not exist.
        """
        pass

    @abstractmethod
    def load_config(self):
        """
        Load database connection parameters from a configuration file.
        """
        pass

    def sanitize_db_name(self, name):
        """
        Validate the database name against length and character restrictions.

        Args:
            name (str): Database name to validate.
        """

        if not isinstance(name, str):
            raise TypeError(f"Database name must be a string, not {type(name)}")

        if len(name) > 63:
            raise ValueError(f"Database name is too long: {len(name)} Max length is 63 characters.")

        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
            raise ValueError(f"{name} must start with letter/underscore. Only letters, numbers, underscores allowed.")

    def create_connection_url(self):
        """
        Construct and return a SQLAlchemy URL object for connecting to the target database.
        Default database URL string is: 'dialect+driver://username:password@host:port/database'

        Returns:
            sqlalchemy.engine.URL: SQLAlchemy connection URL.
        """

        connection_url = URL.create(
            drivername=f"{self.dialect}+{self.driver}",
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db_name
        )
        return connection_url

    def initialize_engine(self, echo=False, **engine_kwargs):
        """
        Create and return a SQLAlchemy engine for the target database.

        Args:
            echo (bool): If True, SQLAlchemy will log all SQL statements.
            **engine_kwargs: Additional arguments passed to `create_engine`.

        Returns:
            sqlalchemy.engine.Engine: SQLAlchemy engine instance.
        """

        connection_url = self.create_connection_url()
        self.engine = create_engine(url=connection_url, echo=echo, **engine_kwargs)
        return self.engine

    def connect_to_fallback_db(self):
        """
        Create a temporary engine to connect to a fallback database
        (e.g., 'postgres', 'information_schema') when the target DB may not exist.

        Returns:
            sqlalchemy.engine.Engine: SQLAlchemy engine connected to fallback DB.
        """

        original_db_name = self.db_name
        self.db_name = self.fallback_database
        temporary_engine = self.initialize_engine(echo=False)
        self.db_name = original_db_name
        return temporary_engine

    @abstractmethod
    def establish_db_connection(self):
        """
        Create or connect to the target database using the initialized configuration.
        To be implemented by subclasses.
        """
        pass

    @abstractmethod
    def database_exists(self):
        """
        Check if the target database already exists.
        To be implemented by subclasses.

        Returns:
            bool: True if database exists, False otherwise.
        """
        pass

    @abstractmethod
    def create_new_database(self, new_db):
        """
        Create a new database with the specified name.
        To be implemented by subclasses.

        Args:
            new_db (str): Name of the new database to create.
        """
        pass
