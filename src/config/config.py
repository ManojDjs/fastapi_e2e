"""
This module provides a configuration class for managing application settings.
The settings can be loaded from environment variables or a configuration file.
"""

import configparser
import os


class Config:
    """
    A class to handle application configuration.
    It supports loading settings from environment variables and a configuration file.
    """

    def __init__(self):
        """
        Initialize the Config instance by loading the configuration file.
        """
        # Load the config file
        self.config = configparser.ConfigParser(
            os.environ, interpolation=configparser.ExtendedInterpolation()
        )
        self.config.read("config.ini")

    def _get_value(self, section, key):
        """
        Retrieve a configuration value.

        Args:
            section (str): The section in the configuration file.
            key (str): The key for the configuration value.

        Returns:
            str: The configuration value, either from the environment variable
            or the configuration file.
        """
        # First check for environment variable, fallback to config file
        env_value = os.getenv(key.upper())
        if env_value is not None:
            return env_value
        return self.config.get(section, key, fallback=None)

    def get_database_url(self):
        """
        Get the database URL.

        Returns:
            str: The database URL from the environment variable or the configuration file.
        """
        return self._get_value("database_url", "DATABASE_URL")

    def get_celery_broker_url(self):
        """
        Get the Celery broker URL.

        Returns:
            str: The Celery broker URL from the environment variable or the configuration file.
        """
        return self._get_value("celery", "CELERY_BROKER_URL")

    def get_celery_results_backend(self):
        """
        Get the Celery results backend URL.

        Returns:
            str: The Celery results backend URL from the environment variable
            or the configuration file.
        """
        return self._get_value("celery", "CELERY_RESULT_BACKEND")

    def get_esm_api_url(self):
        """
        Get the ESM API URL.

        Returns:
            str: The ESM API URL from the environment variable or the configuration file.
        """
        return self._get_value("esm", "ESM_API_URL")

    def get_log_level(self):
        """
        Get the logging level.

        Returns:
            str: The logging level from the environment variable or the configuration file.
        """
        return self._get_value("logging", "LOG_LEVEL")

    def get_thor_api_url(self):
        """
        Get the Thor API URL.

        Returns:
            str: The Thor API URL from the environment variable or the configuration file.
        """
        return self._get_value("thor", "THOR_API_URL")

    def get_spe_api_url(self):
        """
        Get the SPE API URL.

        Returns:
            str: The SPE API URL from the environment variable or the configuration file.
        """
        return self._get_value("spe", "SPE_API_URL")


# Initialize Config instance
config = Config()
