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

import os
import logging
import datetime
import platform
from cushy_storage import utils

logger = logging.getLogger("cushy-storage")


def get_logger():
    return logger


def _check_log_path():
    """check whether log file exist"""
    if not os.path.exists(utils.get_default_log_path()):
        os.makedirs(utils.get_default_log_path())


def get_log_name() -> str:
    _check_log_path()
    cur_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{utils.get_default_log_path()}/log_{cur_time}.log"


def enable_log():
    """enable logging to terminal and file"""
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] %(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(f"{get_log_name()}", mode="w", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def enable_log_no_file():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] %(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
