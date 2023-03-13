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

import time
import unittest
from cushy_storage import CushyDict, disk_cache


class TestDiskCache(unittest.TestCase):
    def test_basic_usage(self):
        @disk_cache('./test-disk-cache')
        def slow_function(x):
            time.sleep(0.1)
            return x + 1

        # Test calling the function with different arguments and caching the output
        self.assertEqual(slow_function(5), 6)
        self.assertEqual(slow_function(5), 6)  # Should use cache this time
        self.assertEqual(slow_function(10), 11)

    def test_serialization(self):
        @disk_cache('./test-disk-cache-serialize', serialize='pickle')
        def slow_function(x):
            time.sleep(0.1)
            return {'result': x}

        # Test caching the output of a function that returns a dictionary using pickle serialization
        self.assertEqual(slow_function(5), {'result': 5})
        self.assertEqual(slow_function(5), {'result': 5})  # Should use cache this time
        self.assertEqual(slow_function(10), {'result': 10})

    def test_compression(self):
        @disk_cache('./test-disk-cache-compress', compress='lzma')
        def slow_function(x):
            time.sleep(0.1)
            return 'a' * (1024 * 1024)

        # Test caching the output of a function that returns a large string using LZMA compression
        self.assertEqual(slow_function(5), 'a' * (1024 * 1024))
        self.assertEqual(slow_function(5), 'a' * (1024 * 1024))  # Should use cache this time
        self.assertEqual(slow_function(10), 'a' * (1024 * 1024))
