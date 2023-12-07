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

from cushy_storage import BaseDict


class TestBaseDict(unittest.TestCase):
    def test_basic_operations(self):
        cache = BaseDict("./cache/test-base-dict")

        # Test adding items to the cache
        cache["foo"] = b"bar"
        self.assertEqual(cache["foo"], b"bar")

        # Test deleting items from the cache
        del cache["foo"]
        with self.assertRaises(KeyError):
            cache["foo"]

        # Test checking if an item is in the cache
        self.assertFalse("foo" in cache)

    def test_compression(self):
        cache = BaseDict("./cache/test-base-dict", compress="lzma")

        # Test storing and retrieving a large string in the cache using LZMA compression
        data = "a" * (1024 * 1024)
        cache["big_data"] = data.encode()
        self.assertEqual(cache["big_data"].decode(), data)
