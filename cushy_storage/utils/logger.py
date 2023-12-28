# Copyright (c) 2023 Zeeland
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright Owner: Zeeland
# GitHub Link: https://github.com/Undertone0809/
# Project Link: https://github.com/Undertone0809/cushy-storage
# Contact Email: zeeland@foxmail.com

import datetime
import logging
import sys
import traceback

from loguru import logger as _logger

from cushy_storage.utils import get_default_storage_path
from cushy_storage.utils.singleton import Singleton

logger = logging.getLogger("cushy-storage")


def get_log_path() -> str:
    log_directory = get_default_storage_path("logs")
    current_time = datetime.datetime.now().strftime("%Y%m%d")
    return f"{log_directory}/{current_time}.log"


def enable_log():
    """
    Enables the logging system to see log information.

    This function configures the logging system to write logs to a file and stderr.
    The log file is located at the path returned by the get_log_path function, and the
    log level for the file is set to DEBUG. The log level for stderr is also set to
    DEBUG.
    """
    log_manager.logger._core.handlers[log_manager.file_logger_id].level = "DEBUG"
    log_manager.logger._core.handlers[log_manager.sys_logger_id].level = "DEBUG"


class LogManager(metaclass=Singleton):
    """
    Logger class that uses the Singleton design pattern.

    This class is responsible for managing the application's logging system. It uses
    the loguru library for logging. The logger is configured to write logs to a file
    and stderr. The log file is located at the path returned by the get_log_path
    function, and the log level for the file is set to DEBUG. The log level for
    stderr is set to WARNING.

    Attributes:
        logger: An instance of the loguru logger.
    """

    def __init__(self) -> None:
        self.logger = _logger

        self.file_logger_id = self.logger.add(
            get_log_path(), level="DEBUG", rotation="1 day"
        )

        # if exist stderr handler, do not add again
        self.sys_logger_id = next(
            (
                handler_id
                for handler_id, handler in self.logger._core.handlers.items()
                if handler._name == "<stderr>"
            ),
            None,
        )

        if self.sys_logger_id is None:
            self.sys_logger_id = self.logger.add(sys.stderr, level="WARNING")


def exception_handler(exc_type, exc_value, exc_traceback):
    """
    Handles uncaught exceptions in the program.

    This function is designed to be used as a custom exception handler. It logs the
    details of uncaught exceptions and allows the program to continue running.
    Exceptions derived from KeyboardInterrupt are not handled by this function and are
    instead passed to the default Python exception handler.

    Args:
        exc_type: The type of the exception.
        exc_value: The instance of the exception.
        exc_traceback: A traceback object encapsulating the call stack at
        the point where the exception originally occurred.

    Returns:
        None
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    tb_info = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logger.error(f"Uncaught exception: {tb_info}")


log_manager = LogManager()
logger = log_manager.logger
sys.excepthook = exception_handler
