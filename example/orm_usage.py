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

from cushy_storage.orm import BaseORMModel, CushyOrmCache


class User(BaseORMModel):
    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age


orm_cache = CushyOrmCache()

"""add user"""
user = User("jack", 18)
orm_cache.add(user)
user = User("jasmine", 18)
orm_cache.add(user)

"""query all user"""
users = orm_cache.query(User).all()
orm_cache.query(User).print_all()

"""query by filter"""
# get all user, you will get a List[User] type data.
# Actually, it will get two users named "jack" and "jasmine".
orm_cache.query("User").filter(age=18).all()
# get first in queryset, you will get a User type data
orm_cache.query("User").filter(name="jack").first()
# filter by multiple parameters
orm_cache.query("User").filter(name="jack", age=18).first()

"""update"""
user = orm_cache.query("User").filter(name="jack").first()
user.age = 18
orm_cache.update_obj(user)

"""delete"""
user = orm_cache.query("User").filter(name="jack").first()
orm_cache.delete(user)
orm_cache.query(User).print_all()
