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


import hashlib
import json
import uuid
from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Tuple, Union

from pydantic import BaseModel, Field
from cushy_storage import CushyDict
from cushy_storage.utils  import get_default_cache_path
from cushy_storage.utils.logger  import logger

class QuerySet:
    def __len__(self):
        return len(self._data)
    
    def __init__(
        self, obj: Union[List[BaseModel], BaseModel], name: Optional[str] = None
    ):
        self._data: List[BaseModel] = obj
        if isinstance(obj, BaseModel):
            self._data = [obj]
        if len(self._data) == 0 and name:
            self.__name__ = name
        else:
            self.__name__ = name if name else self._data[0].__class__.__name__

    @classmethod
    def _from_filter(
        cls, obj: Union[List[BaseModel], BaseModel], name: Optional[str] = None
    ) -> "QuerySet":
        """generate a new queryset from filter"""
        return cls(obj, name)

    def filter(self, **kwargs) -> "QuerySet":
        """
        filter by specified parameter
        Args:
            **kwargs: The property of the object you want to query

        Returns: return a new QuerySet object

        Examples:
            class User(BaseORMModel):
                def __init__(self, name, age):
                    super().__init__()
                    self.name  = name
                    self.age  = age
            # get all user, you will get a List[User] type data.
            # Actually, it will get two users named "jack" and "jasmine".
            orm_cache.query("User").filter(age=18).all() 
            # get first in queryset, you will get a User type data
            orm_cache.query("User").filter(name="jack").first() 
            # filter by multiple parameters
            orm_cache.query("User").filter(name="jack",  age=18).first()
        """
        result: List[BaseModel] = []
        for item in self._data:
            is_target = True
            for query_key, query_value in kwargs.items():
                if getattr(item, query_key, None) != query_value:
                    is_target = False
                    break
            if is_target:
                result.append(item)
        return self._from_filter(result, self.__name__)

    def all(self) -> Optional[List]:
        return self._data

    def first(self):
        if len(self._data) == 0:
            return None
        return self._data[0]

    def print_all(self):
        for item in self._data:
            print(f"[cushy-storage orm] {item.__dict__}")

    @classmethod
    def _from_remove_duplicates(
        cls, obj: List[BaseModel], name: Optional[str] = None
    ) -> "QuerySet":
        return cls(obj, name)

    def remove_duplicates(self) -> Optional["QuerySet"]:
        if len(self._data) == 0:
            return None

        seen_hashes = set()
        unique_objects = []
        
        for obj in self._data:
            
            data = obj.model_dump(exclude={"uid"})
            json_str = json.dumps(data, sort_keys=True)
            obj_hash = hashlib.sha256(json_str.encode()).hexdigest()
            
            if obj_hash not in seen_hashes:
                seen_hashes.add(obj_hash)
                unique_objects.append(obj)
        
        return self._from_remove_duplicates(unique_objects, name=self.__name__)


def _get_class_name(class_name_or_obj: Union[str, type(BaseModel)]) -> str:
    class_name = class_name_or_obj
    if isinstance(class_name_or_obj, type(BaseModel)):
        class_name = class_name_or_obj.__name__
    return class_name


def _get_obj_name(obj: Union[BaseModel, QuerySet, List[BaseModel]]) -> str:
    if isinstance(obj, BaseModel) or isinstance(obj, QuerySet):
        return obj.__name__
    elif isinstance(obj, List):
        return obj[0].__name__


class ORMMixin(ABC):
    def _get_original_data_from_cache(self, class_name_or_obj) -> List[BaseModel]:
        class_name = _get_class_name(class_name_or_obj)
        if class_name not in self:
            self.__setitem__(class_name, [])
        return self.__getitem__(class_name)

    def query(self, class_name_or_obj: Union[str, type(BaseModel)]) -> QuerySet:
        """query all objects by class name"""
        logger.info(f"[orm]  query all objects, class name {class_name_or_obj}")
        original_result = self._get_original_data_from_cache(class_name_or_obj)
        if len(original_result) == 0:
            return QuerySet(original_result, name=_get_class_name(class_name_or_obj))
        return QuerySet(original_result)

    def remove_duplicates(self) -> "QuerySet":
        if not self._data:
            return self

        seen = set()
        unique_objects = []
        for obj in self._data:
            data = obj.model_dump(exclude={"uid"})
            json_str = json.dumps(data, sort_keys=True)
            obj_hash = hashlib.sha256(json_str.encode()).hexdigest()

            if obj_hash not in seen:
                seen.add(obj_hash)
                unique_objects.append(obj)

        return self.__class__(unique_objects, self.__name__)

    def add(self, obj: Union[BaseModel, QuerySet, List[BaseModel]]) -> QuerySet:
        logger.info(f"[orm] add object, object {obj}")
        obj_name = _get_obj_name(obj)
        original_result: List[BaseModel] = self._get_original_data_from_cache(obj_name)

        if isinstance(obj, BaseModel):
            if obj not in original_result:
                original_result.append(obj) 
        elif isinstance(obj, QuerySet):
            for item in obj.all(): 
                if item not in original_result:
                    original_result.append(item) 
        else:
            for item in obj:
                if item not in original_result:
                    original_result.append(item) 

        self[obj_name] = original_result 
        return QuerySet(self[obj_name])

    def delete(self, obj: Union[List[BaseModel], QuerySet, BaseModel]):
        """Deletion via object UID (batch supported)"""
        logger.info(f"[orm]  delete object, object {obj}")
        obj_name = _get_obj_name(obj)
        original_data: List[BaseModel] = self._get_original_data_from_cache(obj_name)
        updated_data = original_data.copy() 

        to_delete = []
        if isinstance(obj, BaseModel):
            to_delete = [obj]
        elif isinstance(obj, QuerySet):
            to_delete = obj.all() 
        elif isinstance(obj, list):
            to_delete = obj

        delete_uids = {item.uid  for item in to_delete}
        updated_data = [item for item in updated_data if item.uid  not in delete_uids]

        self[obj_name] = updated_data

    def delete_by(self, cls: type(BaseModel), **conditions):
        """Delete objects directly from conditional parameters"""
        queryset = self.query(cls).filter(**conditions) 
        if queryset.all(): 
            self.delete(queryset.all()) 

    def set(self, obj: Union[BaseModel, QuerySet, List[BaseModel]]):
        logger.info(f"[orm]     set object, object {obj}")
        obj_name = _get_obj_name(obj)
 
        if isinstance(obj, BaseModel):
            obj_list = [obj]
        elif isinstance(obj, QuerySet):
            obj_list = obj.all() 
        else:
            obj_list = obj 
            
        seen_uids = set()
        unique_objs = []
        for o in obj_list:
            if o.uid  not in seen_uids:
                seen_uids.add(o.uid) 
                unique_objs.append(o) 
 
        self[obj_name] = unique_objs

    def __getitem__(self, item) -> List[BaseModel]:
        """implemented by CushyDict"""

    def __setitem__(self, key, value) -> List[BaseModel]:
        """implemented by CushyDict"""


class CushyOrmCache(CushyDict, ORMMixin):
    def __init__(
        self,
        path: str = get_default_cache_path(),
        compress: Union[str, Tuple[Callable, Callable], None] = None,
    ):
        super().__init__(path, compress, "pickle")
        
    
    def update(self, obj: BaseModel):
        """Update an existing object in the cache based on its uid."""
        logger.info(f"[orm] update object, object {obj}")
        obj_name = _get_obj_name(obj)
        original_data: List[BaseModel] = self._get_original_data_from_cache(obj_name)

        for i, item in enumerate(original_data):
            if item.uid == obj.uid:
                original_data[i] = obj
                break

        self[obj_name] = original_data  