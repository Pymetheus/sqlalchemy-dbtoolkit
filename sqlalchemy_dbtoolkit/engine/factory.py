from sqlalchemy_dbtoolkit.engine.mysql_engine import MysqlEngine
from sqlalchemy_dbtoolkit.engine.postgresql_engine import PostgreSQLEngine
from sqlalchemy_dbtoolkit.engine.sqlite_engine import SqliteEngine


class AlchemyEngineFactory:
    """
    Factory class to initialize and return the appropriate SQLAlchemy engine instance
    for a supported database management system (DBMS).

    Currently, supports MySQL and SQLite engines.
    """

    def __init__(self, dbms, db_name, config_path='../../.config/config.ini'):
        """
        Initializes the AlchemyEngineFactory with the specified DBMS and database name.

        Args:
            dbms (str): Type of database management system (e.g., 'mysql', 'postgresql', 'sqlite').
            db_name (str): Name of the target database.
            config_path (str): Path to the configuration file. Defaults to '../../.config/config.ini'.
        """

        self.dbms = dbms
        self.db_name = db_name
        self.config_path = config_path

        self.validate_supported_dbms()
        self.engine = self.initialize_engine()

    def validate_supported_dbms(self):
        """
        Validates that the provided DBMS is supported.
        """
        supported_dbms = ['mysql', 'postgresql', 'sqlite']
        if self.dbms not in supported_dbms:
            raise ValueError(f"{self.dbms} is not in supported DBMS: {supported_dbms}")

    def initialize_engine(self):
        """
        Instantiates and initializes the appropriate engine class
        based on the selected DBMS.

        Returns:
            sqlalchemy.engine.Engine: Initialized SQLAlchemy engine.
        """

        if self.dbms == 'mysql':
            engine_instance = MysqlEngine(db_name=self.db_name, config_path=self.config_path)
            engine_instance.establish_db_connection()
            return engine_instance.engine
        elif self.dbms == 'postgresql':
            engine_instance = PostgreSQLEngine(db_name=self.db_name, config_path=self.config_path)
            engine_instance.establish_db_connection()
            return engine_instance.engine
        elif self.dbms == 'sqlite':
            engine_instance = SqliteEngine(db_name=self.db_name, config_path=self.config_path)
            engine_instance.establish_db_connection()
            return engine_instance.engine
