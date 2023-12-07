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
import tempfile


def get_project_root_path() -> str:
    """get project root path"""
    project_path = os.getcwd()
    max_depth = 10
    count = 0
    while not os.path.exists(os.path.join(project_path, "README.md")):
        project_path = os.path.split(project_path)[0]
        count += 1
        if count > max_depth:
            return os.getcwd()
    return project_path


def convert_backslashes(path: str):
    """Convert all \\ to / of file path."""
    return path.replace("\\", "/")


def get_default_storage_path(module_name: str = "") -> str:
    pne_storage_path = os.path.expanduser("~/.cushy-storage")

    if not os.path.exists(pne_storage_path):
        try:
            os.makedirs(pne_storage_path)
        except PermissionError:
            pne_storage_path = f"{tempfile.gettempdir()}/cushy-storage"

    return convert_backslashes(f"{pne_storage_path}/{module_name}")


def get_default_cache_path() -> str:
    return get_default_storage_path("cache")


def get_default_log_path() -> str:
    return get_default_storage_path("log")
