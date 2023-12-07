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
from abc import ABC
from typing import Callable, List, Optional, Tuple, Union

from cushy_storage import CushyDict
from cushy_storage.utils import get_default_cache_path
from cushy_storage.utils.logger import logger


class BaseORMModel(ABC):
    def __init__(self):
        self.__name__ = type(self).__name__
        self.__unique_id__: str = str(uuid.uuid4())

    def __get_element_hash__(self) -> str:
        dic = self.__dict__.copy()
        del dic["__unique_id__"]

        json_data = json.dumps(dic, sort_keys=True).encode("utf-8")
        hash256 = hashlib.sha256()
        hash256.update(json_data)
        return hash256.hexdigest()


class QuerySet:
    def __init__(
        self, obj: Union[List[BaseORMModel], BaseORMModel], name: Optional[str] = None
    ):
        self._data: List[BaseORMModel] = obj
        if isinstance(obj, BaseORMModel):
            self._data = [obj]
        if len(self._data) == 0 and name:
            self.__name__ = name
        else:
            self.__name__ = name if name else self._data[0].__name__

    @classmethod
    def _from_filter(
        cls, obj: Union[List[BaseORMModel], BaseORMModel], name: Optional[str] = None
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
                    self.name = name
                    self.age = age
            # get all user, you will get a List[User] type data.
            # Actually, it will get two users named "jack" and "jasmine".
            orm_cache.query("User").filter(age=18).all()
            # get first in queryset, you will get a User type data
            orm_cache.query("User").filter(name="jack").first()
            # filter by multiple parameters
            orm_cache.query("User").filter(name="jack", age=18).first()
        """
        result: List[BaseORMModel] = []
        for item in self._data:
            is_target = True
            for query_key in kwargs.keys():
                if item.__dict__[query_key] != kwargs[query_key]:
                    is_target = False
                    continue
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
        cls, obj: List[BaseORMModel], name: Optional[str] = None
    ) -> "QuerySet":
        return cls(obj, name)

    def remove_duplicates(self) -> Optional["QuerySet"]:
        if len(self._data) == 0:
            return None

        result_element_hash = []
        result: List[BaseORMModel] = []
        for obj in self._data:
            if obj.__get_element_hash__() not in result_element_hash:
                result_element_hash.append(obj.__get_element_hash__())
                result.append(obj)
        return self._from_remove_duplicates(result, name=self.__name__)


def _get_class_name(class_name_or_obj: Union[str, type(BaseORMModel)]) -> str:
    class_name = class_name_or_obj
    if isinstance(class_name_or_obj, type(BaseORMModel)):
        class_name = class_name_or_obj.__name__
    return class_name


def _get_obj_name(obj: Union[BaseORMModel, QuerySet, List[BaseORMModel]]) -> str:
    if isinstance(obj, BaseORMModel) or isinstance(obj, QuerySet):
        return obj.__name__
    elif isinstance(obj, List):
        return obj[0].__name__


class ORMMixin(ABC):
    def _get_original_data_from_cache(
        self, class_name_or_obj: Union[str, type(BaseORMModel)]
    ) -> List[BaseORMModel]:
        class_name = _get_class_name(class_name_or_obj)
        if class_name not in self:
            self.__setitem__(class_name, [])
        return self.__getitem__(class_name)

    def query(self, class_name_or_obj: Union[str, type(BaseORMModel)]) -> QuerySet:
        """query all objects by class name"""
        logger.info(f"[orm] query all objects, class name {class_name_or_obj}")
        original_result = self._get_original_data_from_cache(class_name_or_obj)
        if len(original_result) == 0:
            return QuerySet(original_result, name=_get_class_name(class_name_or_obj))
        return QuerySet(original_result)

    def remove_duplicates(self, class_name_or_obj: Union[type(BaseORMModel), str]):
        logger.info(f"[orm] remove duplicates, class name {class_name_or_obj}")
        original_result = self._get_original_data_from_cache(class_name_or_obj)
        if len(original_result) != 0:
            queryset = QuerySet(original_result)
            queryset = queryset.remove_duplicates()
            self.set(queryset)

    def add(self, obj: Union[BaseORMModel, QuerySet, List[BaseORMModel]]) -> QuerySet:
        logger.info(f"[orm] add object, object {obj}")
        obj_name = _get_obj_name(obj)
        original_result: List[BaseORMModel] = self._get_original_data_from_cache(
            obj_name
        )

        if isinstance(obj, BaseORMModel):
            original_result.append(obj)
        elif isinstance(obj, QuerySet):
            original_result += obj.all()
        else:
            original_result += obj

        self[obj_name] = original_result
        return QuerySet(self[obj_name])

    def delete(self, obj: Union[List[BaseORMModel], QuerySet, BaseORMModel]):
        """delete obj by obj.__unique_id__"""
        logger.info(f"[orm] delete object, object {obj}")
        obj_name = _get_obj_name(obj)
        original_result: List[BaseORMModel] = self._get_original_data_from_cache(
            obj_name
        )
        copy_result: List[BaseORMModel] = original_result.copy()

        if isinstance(obj, BaseORMModel):
            obj = [obj]
        elif isinstance(obj, QuerySet):
            obj = obj.all()
        if len(obj) == 0:
            return

        for cache_obj_item in original_result:
            for input_obj_item in obj:
                if cache_obj_item.__unique_id__ == input_obj_item.__unique_id__:
                    copy_result.remove(cache_obj_item)
        return self.__setitem__(obj_name, copy_result)

    def set(self, obj: Union[BaseORMModel, QuerySet, List[BaseORMModel]]):
        logger.info(f"[orm] set object, object {obj}")
        obj_name = _get_obj_name(obj)
        if isinstance(obj, BaseORMModel):
            obj = [obj]
        elif isinstance(obj, QuerySet):
            obj = obj.all()
        if len(obj) == 0:
            return
        return self.__setitem__(obj_name, obj)

    def update_obj(self, obj: BaseORMModel):
        logger.info(f"[orm] update object, object {obj}")
        original_result: List[BaseORMModel] = self._get_original_data_from_cache(
            obj.__name__
        )
        copy_result: List[BaseORMModel] = original_result.copy()

        for i in range(len(copy_result)):
            if copy_result[i].__unique_id__ == obj.__unique_id__:
                copy_result[i] = obj
                return self.__setitem__(obj.__name__, copy_result)

        raise ValueError(f"can not found object: {obj}")

    def __getitem__(self, item) -> List[BaseORMModel]:
        """implemented by CushyDict"""

    def __setitem__(self, key, value) -> List[BaseORMModel]:
        """implemented by CushyDict"""


class CushyOrmCache(CushyDict, ORMMixin):
    def __init__(
        self,
        path: str = get_default_cache_path(),
        compress: Union[str, Tuple[Callable, Callable], None] = None,
    ):
        super().__init__(path, compress, "pickle")
