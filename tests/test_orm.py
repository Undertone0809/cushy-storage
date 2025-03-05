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
import uuid
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from cushy_storage.orm import CushyOrmCache, QuerySet
from tests.utils  import delete_cache

cache_file = {
    "test_orm_add_and_query": "./cache/test-cushy-orm-cache",
    "test_orm_delete": "./cache/test-cushy-orm-cache-orm-delete",
    "test_orm_update": "./cache/test-cushy-orm-cache-orm-update",
    "test_orm_set": "./cache/test-cushy-orm-cache-orm-set",
    "test_orm_remove_duplicates": "./cache/test-cushy-orm-cache-orm-remove-duplicates",
}

class User(BaseModel):
    name: str
    age: int
    uid: str = Field(default_factory=lambda: str(uuid.uuid4())) 
    __name__: str = "User"

class TestORM(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        delete_cache()

    def test_queryset_base(self):
        user_list: List[User] = [
            User(name="jack", age=18),
            User(name="jasmine", age=18)
        ]
        queryset = QuerySet(user_list)

        # assert all() and first()
        self.assertEqual(len(queryset.all()),  2)
        self.assertEqual(queryset.first().name,  "jack")
        self.assertEqual(queryset.first().age,  18)

        # assert filter()
        queried_user = queryset.filter(name="jack").first() 
        self.assertEqual(queried_user.name,  "jack")
        self.assertEqual(queried_user.age,  18)

        # filter with multiple params
        queried_users = queryset.filter(name="jack",  age=18).all()
        self.assertEqual(len(queried_users),  1)
        self.assertEqual(queried_users[0].name,  "jack")
        self.assertEqual(queried_users[0].age,  18)

        # filter multiple result
        queried_users = queryset.filter(age=18).all() 
        self.assertEqual(len(queried_users),  2)
        self.assertEqual(queried_users[0].name,  "jack")
        self.assertEqual(queried_users[1].name,  "jasmine")

        # filter by multiple parameters
        queried_user = queryset.filter(name="jack",  age=18).first()
        self.assertEqual(queried_user.name,  "jack")
        self.assertEqual(queried_user.age,  18)

    def test_orm_add_and_query(self):
        orm_cache = CushyOrmCache(cache_file["test_orm_add_and_query"])
        user = User(name="jack", age=18)
        
        # assert add()
        queryset = orm_cache.add(user) 
        self.assertEqual(len(queryset.all()),  1)

        # assert query()
        queryset_by_class = orm_cache.query(User) 
        self.assertEqual(queryset_by_class.first().name,  "jack")
        self.assertEqual(queryset_by_class.first().age,  18)

        queryset_by_str = orm_cache.query("User") 
        self.assertEqual(queryset_by_str.first().name,  "jack")
        self.assertEqual(queryset_by_str.first().age,  18)

        # add multiple users
        user_list: List[User] = [
            User(name="zeeland", age=22),
            User(name="hizeros", age=20),
            User(name="honey", age=18),
        ]
        queryset = orm_cache.add(user_list) 
        self.assertEqual(len(queryset.all()),  4)
        self.assertIsNotNone(queryset.filter(name="zeeland").first()) 

    def test_orm_delete(self):
        orm_cache = CushyOrmCache(cache_file["test_orm_delete"])

        users = [
            User(name="user a", age=20),
            User(name="user b", age=30),
            User(name="user c", age=40)
        ]
        
        original_uids = {u.uid  for u in users}
        
        orm_cache.add(users) 
        
        orm_cache.delete_by(User, name="user b")

        remaining = orm_cache.query(User).all() 
        self.assertEqual(len(remaining),  2)

        remaining_uids = {u.uid  for u in remaining}
        
        self.assertTrue(original_uids.issuperset(remaining_uids)) 

        deleted_user = orm_cache.query(User).filter(name="user  b").first()
        self.assertIsNone(deleted_user) 

    def test_orm_update(self):
        orm_cache = CushyOrmCache(cache_file["test_orm_update"])
        user = User(name="old username", age=18)
        original_uid = user.uid 
        orm_cache.add(user) 
        
        user.name = "new username"
        user.age = 25
        orm_cache.update(user)
        
        queried = orm_cache.query(User).filter(name="new username").all()
        self.assertEqual(len(queried), 1)
        
        updated_user = queried[0]
        
        self.assertEqual(updated_user.uid, original_uid)
        self.assertEqual(updated_user.name, "new username")
        self.assertEqual(updated_user.age, 25)

    def test_orm_set(self):
        orm_cache = CushyOrmCache(cache_file["test_orm_set"])
        
        users = [User(name="no exist user", age=18) for _ in range(10)]
        orm_cache.add(users) 
        
        self.assertEqual(len(orm_cache.query(User).all()),  10)
        
        orm_cache.set(User(name="existing user", age=10))
        queryset = orm_cache.query(User).all() 
        self.assertEqual(len(queryset),  1)
        self.assertEqual(queryset[0].name, "existing user")

    def test_orm_remove_duplicates(self):
        orm_cache = CushyOrmCache(cache_file["test_orm_remove_duplicates"])
        users = []
        
        for i in range(10):
            users.append(User(name="user1",  age=1))
            users.append(User(name="last user", age=18))
            
        
        orm_cache.add(users) 
        self.assertEqual(len(orm_cache.query(User).all()), 20)
        
        queryset = orm_cache.query(User).remove_duplicates()
        orm_cache.set(queryset.all())
        self.assertEqual(len(queryset),  2)