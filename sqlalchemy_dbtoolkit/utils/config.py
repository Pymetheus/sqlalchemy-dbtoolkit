import os
import configparser


class Config:
    """
    Loads database configuration from INI file.
    """

    def __init__(self, config_path='../../.config/config.ini'):
        """
        Initialize Config with the path to the INI file.
        Args:
            config_path (str): Path to the configuration file.
        """

        self.config_path = config_path
        self.config = self.import_config()

    def validate_config_path(self):
        """
        Raise error if config path does not exist.
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found in: {self.config_path}")

    def import_config(self):
        """
        Parse and return the configuration object.
        """
        self.validate_config_path()
        config = configparser.ConfigParser(interpolation=None)
        config.read(self.config_path)
        return config

    @property
    def mysql_host(self):
        """
        Return MySQL host.
        """
        try:
            return self.config["mysql"]["host"]
        except KeyError:
            raise KeyError("Missing 'mysql host' under [mysql] section.")

    @property
    def mysql_user(self):
        """
        Return MySQL user.
        """
        try:
            return self.config["mysql"]["user"]
        except KeyError:
            raise KeyError("Missing 'mysql user' under [mysql] section.")

    @property
    def mysql_password(self):
        """
        Return MySQL password.
        """
        try:
            return self.config["mysql"]["password"]
        except KeyError:
            raise KeyError("Missing 'mysql password' under [mysql] section.")

    @property
    def mysql_port(self):
        """
        Return MySQL port.
        """
        try:
            return self.config["mysql"]["port"]
        except KeyError:
            raise KeyError("Missing 'mysql port' under [mysql] section.")

    @property
    def postgresql_host(self):
        """
        Return PostgreSQL host.
        """
        try:
            return self.config["postgresql"]["host"]
        except KeyError:
            raise KeyError("Missing 'postgresql host' under [postgresql] section.")

    @property
    def postgresql_user(self):
        """
        Return PostgreSQL user.
        """
        try:
            return self.config["postgresql"]["user"]
        except KeyError:
            raise KeyError("Missing 'postgresql user' under [postgresql] section.")

    @property
    def postgresql_password(self):
        """
        Return PostgreSQL password.
        """
        try:
            return self.config["postgresql"]["password"]
        except KeyError:
            raise KeyError("Missing 'postgresql password' under [postgresql] section.")

    @property
    def postgresql_port(self):
        """
        Return PostgreSQL port.
        """
        try:
            return self.config["postgresql"]["port"]
        except KeyError:
            raise KeyError("Missing 'postgresql port' under [postgresql] section.")

    @property
    def sqlite_path(self):
        """
        Return SQLite file path.
        """
        try:
            return self.config["sqlite"]["path"]
        except KeyError:
            raise KeyError("Missing 'sqlite path' under [sqlite] section.")
