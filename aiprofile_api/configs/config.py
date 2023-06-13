import configparser
import multiprocessing
import os
from aiprofile_api.configs.constants import DEV
from typing import Dict, Any
from flask import app as flask_app

config = configparser.RawConfigParser()
config.read("{}/{}".format(os.path.join(os.path.dirname(__file__)), "config.ini"))
ENV = os.environ.get("FLASK_ENV", DEV)


class Config:
    ENV: str
    DEBUG: str
    WORKERS: int
    HOST: str
    PORT: str
    LOGGING_TYPE: str
    DEBUG_TB_INTERCEPT_REDIRECTS: str
    CACHE_TYPE: str
    ASSETS_DEBUG: str
    RELOADED: str



    def load_config(self):
        self.ENV = os.getenv("ENV", config.get(ENV, "env", fallback="dev"))
        self.DEBUG = os.getenv("DEBUG", config.getboolean(ENV, "debug", fallback="false"))
        self.WORKERS = os.getenv("WORKERS", multiprocessing.cpu_count() * 2 + 1)
        self.HOST = os.getenv("HOST", config.get(ENV, "host", fallback="0.0.0.0"))
        self.PORT = os.getenv("PORT", config.getint(ENV, "port", fallback="5052"))
        self.LOGGING_TYPE = os.getenv("LOGGING_TYPE", config.get(ENV, "logging_type", fallback="ERROR"))
        self.DEBUG_TB_INTERCEPT_REDIRECTS = os.getenv("DEBUG_TB_INTERCEPT_REDIRECTS", config.getboolean(ENV, "debug_tb_intercept_redirects", fallback="false"))
        self.ASSETS_DEBUG = os.getenv("ASSETS_DEBUG", config.getboolean(ENV, "assets_debug", fallback="false"))
        self.CACHE_TYPE = os.getenv("CACHE_TYPE", config.get(ENV, "cache_type", fallback=""))
        self.RELOADED = os.getenv("RELOADED", config.getboolean(ENV, "reloaded", fallback="false"))



    def get_config(self) -> Dict[str, Any]:
        """Get config and turn it into dictionary
        :return: dictionary object
        """
        return self.__dict__

    @staticmethod
    def read_config(

    ):
        """Load config from class it self
        :return: config class
        """
        config_data = Config()
        config_data.load_config()
        return config_data


def config_from_ini(app: flask_app):
    """Append configuration from ini file to flask config
    :param app: flask config object
    :return: None
    """
    cfg = Config()
    cfg.load_config()
    app.config.from_object(cfg)
