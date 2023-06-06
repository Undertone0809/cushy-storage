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
from typing import List

from cushy_storage.orm import QuerySet
from cushy_storage import CushyOrmCache, BaseORMModel
from cushy_storage.logger import enable_log
from tests.utils import delete_cache

cache_file = {
    "test_orm_add_and_query": "./cache/test-cushy-orm-cache",
    "test_orm_delete": "./cache/test-cushy-orm-cache-orm-delete",
    "test_orm_update": "./cache/test-cushy-orm-cache-orm-update",
}
enable_log()


class User(BaseORMModel):

    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age


class TestORM(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        delete_cache()

    def test_queryset_base(self):
        user_list: List[User] = [User("jack", 18), User("jasmine", 18)]
        queryset = QuerySet(user_list)

        # assert all() and first()
        self.assertEqual(len(queryset.all()), 2)
        self.assertEqual(queryset.first().name, "jack")
        self.assertEqual(queryset.first().age, 18)

        # assert filter()
        queried_user = queryset.filter(name="jack").first()
        self.assertEqual(queried_user.name, "jack")
        self.assertEqual(queried_user.age, 18)

        # filter multiple result
        queried_users = queryset.filter(age=18).all()
        self.assertEqual(len(queried_users), 2)
        self.assertEqual(queried_users[0].name, "jack")
        self.assertEqual(queried_users[1].name, "jasmine")

        # filter by multiple parameters
        queried_user = queryset.filter(name="jack", age=18).first()
        self.assertEqual(queried_user.name, "jack")
        self.assertEqual(queried_user.age, 18)

    def test_orm_add_and_query(self):
        orm_cache = CushyOrmCache(cache_file['test_orm_add_and_query'])
        user = User("jack", 18)
        # assert add()
        queryset = orm_cache.add(user)
        self.assertEqual(len(queryset.all()), 1)

        # assert query()
        queryset_by_class = orm_cache.query(User)
        self.assertEqual(queryset_by_class.first().name, "jack")
        self.assertEqual(queryset_by_class.first().age, 18)

        queryset_by_str = orm_cache.query("User")
        self.assertEqual(queryset_by_str.first().name, "jack")
        self.assertEqual(queryset_by_str.first().age, 18)

        # add more user
        user = User("jasmine", 22)
        queryset = orm_cache.add(user)
        self.assertEqual(len(queryset.all()), 2)

    def test_orm_delete(self):
        orm_cache = CushyOrmCache(cache_file['test_orm_delete'])

        # add single user
        user_a = User("user a", 20)
        orm_cache.add(user_a)
        user_b = User("user b", 30)
        orm_cache.add(user_b)
        user_c = User("user c", 40)
        orm_cache.add(user_c)

        self.assertEqual(len(orm_cache.query(User).all()), 3)
        orm_cache.query(User).print_all()

        # delete single user
        orm_cache.delete(user_b)
        orm_cache.query(User).print_all()
        queryset = orm_cache.query(User)
        self.assertEqual(len(queryset.all()), 2)
        self.assertEqual(queryset.first().name, "user a")
        self.assertEqual(queryset.first().age, 20)

    def test_orm_update(self):
        orm_cache = CushyOrmCache(cache_file['test_orm_update'])
        user = User("old username", 18)
        orm_cache.add(user)

        # assert update
        user.name = "new username"
        orm_cache.update_obj(user)
        queried_user = orm_cache.query(User).filter(name="new username").first()
        self.assertIsNotNone(queried_user)
        self.assertEqual(queried_user.name, "new username")
