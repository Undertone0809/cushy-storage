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

from typing import List

BASE_TYPE = [int, str, float, dict, list, tuple, bytes]


class EnhancedList(list):
    """Custom List to provide more functions"""

    def append(self, __object) -> List:
        super().append(__object)
        return self

    def remove(self, __value) -> List:
        super().remove(__value)
        return self

    def insert(self, __index, __object) -> List:
        super().insert(__index, __object)
        return self

    def reverse(self) -> List:
        super().reverse()
        return self
