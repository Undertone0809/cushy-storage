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

import unittest
from cushy_storage import CushyDict


class TestCushyDict(unittest.TestCase):
    def test_read_and_write_data(self):
        cache = CushyDict("./test-cache")
        cache['a'] = 10
        self.assertEqual(cache['a'], 10)

        cache['b'] = "test"
        self.assertEqual(cache['b'], "test")

        cache['c'] = [1, 2, 3, 4]
        self.assertEqual(cache['c'], [1, 2, 3, 4])

        cache['d'] = {"key": "value"}
        self.assertEqual(cache['d'], {"key": "value"})

        cache['e'] = ("hello", 1)
        print(type(cache['e']))
        self.assertEqual(cache['e'], ["hello", 1])

    def test_data_type(self):
        cache = CushyDict("./test-cache")
        self.assertEqual(type(cache['a']), int)
        self.assertEqual(type(cache['b']), str)
        self.assertEqual(type(cache['c']), list)
        self.assertEqual(type(cache['d']), dict)
        # todo https://github.com/Undertone0809/cushy-stroage/issues/1
        self.assertEqual(type(cache['e']), list)
