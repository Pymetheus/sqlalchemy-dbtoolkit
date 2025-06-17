from sqlalchemy_dbtoolkit.utils.config import Config
from sqlalchemy_dbtoolkit.engine.builder import BaseEngine
from sqlalchemy import text


class MysqlEngine(BaseEngine):
    """
    MySQL-specific implementation of the BaseEngine abstract class.

    Manages engine initialization, configuration loading, and database creation for MySQL databases.
    """

    def __init__(self, db_name, config_path='../../.config/config.ini'):
        """
        Initializes the MysqlEngine with the given database name and config path.

        Args:
            db_name (str): Name of the MySQL database.
            config_path (str): Path to the configuration file. Defaults to '../../.config/config.ini'.
        """

        super().__init__(db_name, config_path)
        self.driver = "mysqlconnector"
        self.load_config()

    @property
    def dialect(self):
        """
        Returns the SQLAlchemy dialect for MySQL.

        Returns:
            str: Always returns 'mysql'.
        """
        return "mysql"

    @property
    def fallback_database(self):
        """
        Provides the fallback database used for administrative operations in MySQL.

        Returns:
            str: The name of the fallback database, 'information_schema'.
        """

        return "information_schema"

    def load_config(self):
        """
        Loads MySQL configuration from the config file.
        """

        try:
            config = Config(config_path=self.config_path)
            self.username = config.mysql_user
            self.password = config.mysql_password
            self.host = config.mysql_host
            self.port = config.mysql_port or self.DEFAULT_DB_PORTS.get(self.dialect)
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
        Checks whether the specified database exists on the MySQL server.

        Returns:
            bool: True if the database exists, False otherwise.
        """

        temp_engine = None
        try:
            temp_engine = self.connect_to_fallback_db()
            with temp_engine.begin() as temp_connection:
                check_db_query = "SHOW DATABASES;"
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
        Creates a new MySQL database if it does not already exist.

        Args:
            new_db (str): Name of the database to be created.
        """

        temp_engine = None
        try:
            temp_engine = self.connect_to_fallback_db()
            with temp_engine.connect() as temp_connection:
                create_db_query = f"CREATE DATABASE IF NOT EXISTS {new_db}"
                temp_connection.execute(text(create_db_query))
                temp_connection.commit()
        except Exception as e:
            raise RuntimeError(f"Failed to create database {new_db}: {e}")
        finally:
            if temp_engine:
                temp_engine.dispose()
