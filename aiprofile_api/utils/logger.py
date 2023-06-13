import logging
import inspect
from typing import Any, Dict
from flask import request
from aiprofile_api.configs import Config
from aiprofile_api.configs.constants import SERVICE_NAME

LOG_TYPE = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "ERROR": logging.ERROR,
    "FATAL": logging.FATAL,
}

cfg = Config()
cfg.load_config()
logging.basicConfig(
    format='{"datetime": "%(asctime)s", "level_name": "%(levelname)s", "message": "%(message)s" }',
    level=LOG_TYPE.get(cfg.LOGGING_TYPE, "INFO"),
)


class Logging:

    @staticmethod
    def get_logger():
        return logging

    @staticmethod
    def formatting_message(
            msg: Any
    ) -> Dict[str, Any]:
        """formatting message to get better logs
        :param msg: message that want to print
        :return: dictionary message
        """
        func_inspection = inspect.stack()
        default_msg = {
            "service_name": SERVICE_NAME,
            "text": msg,
            "func_name": "{}:{}".format(func_inspection[2].function, func_inspection[2].lineno),
            "func_file_path": func_inspection[2].filename,
        }
        try:
            default_msg["url"] = request.url
            default_msg["payload"] = request.get_json()
            default_msg["query_string"] = dict(request.args)
            return default_msg
        except RuntimeError:
            # when entering this exception means
            # logging come from scheduler and not from flask server
            return default_msg

    @staticmethod
    def info(message: Any):
        """Print logging info message
        :param message: any message
        :return: None
        """
        logging.info(Logging.formatting_message(message))

    @staticmethod
    def debug(message: Any):
        """Print logging debug message
        :param message: any message
        :return: None
        """
        logging.debug(Logging.formatting_message(message))

    @staticmethod
    def error(message: Any):
        """Print logging error message
        :param message: any message
        :return: None
        """
        logging.error(Logging.formatting_message(message))

    @staticmethod
    def warning(message: Any):
        """Print logging warning message
        :param message: any message
        :return: None
        """
        logging.warning(Logging.formatting_message(message))

    @staticmethod
    def exception(message: Any):
        """Print logging exception() message
        :param message: any message
        :return: None
        """
        logging.exception(Logging.formatting_message(message))
