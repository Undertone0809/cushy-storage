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

import uuid
from abc import ABC
from typing import Union, Tuple, Callable, List, Optional

from cushy_storage import CushyDict
from cushy_storage.utils import get_default_cache_path


class BaseORMModel(ABC):

    def __init__(self):
        self.__name__ = type(self).__name__
        self._unique_id = str(uuid.uuid4())


class QuerySet:

    def __init__(self, obj: Union[List[BaseORMModel], BaseORMModel], name: Optional[str] = None):
        self._data: List[BaseORMModel] = obj
        if isinstance(obj, BaseORMModel):
            self._data = [obj]
        self.__name__ = name if name else self._data[0].__name__

    @classmethod
    def _from_filter(cls, obj: Union[List[BaseORMModel], BaseORMModel]):
        """generate a new queryset from filter"""
        return cls(obj)

    def filter(self, **kwargs):
        result: List[BaseORMModel] = []
        for item in self._data:
            for query_key in kwargs.keys():
                if item.__dict__[query_key] != kwargs[query_key]:
                    continue
                result.append(item)

        return self._from_filter(result)

    def all(self) -> Optional[List[BaseORMModel]]:
        return self._data

    def first(self) -> Optional[BaseORMModel]:
        if len(self._data) == 0:
            return None
        return self._data[0]

    def print_all(self):
        for item in self._data:
            print(f"[cushy-storage orm] {item.__dict__}")


def _get_class_name(class_name_or_obj: Union[str, type(BaseORMModel)]) -> str:
    class_name: str = class_name_or_obj
    if isinstance(class_name_or_obj, type(BaseORMModel)):
        class_name = class_name_or_obj.__name__
    return class_name


class ORMMixin(ABC):

    def _get_original_data_from_cache(self, class_name_or_obj: Union[str, type(BaseORMModel)]) -> List[BaseORMModel]:
        class_name = _get_class_name(class_name_or_obj)
        if class_name not in self:
            self.__setitem__(class_name, [])
        return self.__getitem__(class_name)

    def query(self, class_name_or_obj: Union[str, type(BaseORMModel)]):
        """query all objects by class name"""
        original_result = self._get_original_data_from_cache(class_name_or_obj)
        if len(original_result) == 0:
            return QuerySet(original_result, name=_get_class_name(class_name_or_obj))
        return QuerySet(original_result)

    def add(self, obj: Union[BaseORMModel, QuerySet]) -> QuerySet:
        original_result = self._get_original_data_from_cache(obj.__name__)

        if isinstance(obj, BaseORMModel):
            original_result.append(obj)
        elif isinstance(obj, QuerySet):
            original_result = original_result + obj.all()
        self.__setitem__(obj.__name__, original_result)
        return QuerySet(self.__getitem__(obj.__name__))

    def delete(self, obj: BaseORMModel):
        """delete obj by obj._unique_id"""
        original_result: List[BaseORMModel] = self._get_original_data_from_cache(obj.__name__)
        copy_result: List[BaseORMModel] = original_result.copy()

        for item in copy_result:
            if item._unique_id == obj._unique_id:
                copy_result.remove(item)
                return self.__setitem__(obj.__name__, copy_result)

        raise ValueError(f"can not found object: {obj}")

    def update_obj(self, obj: BaseORMModel):
        original_result: List[BaseORMModel] = self._get_original_data_from_cache(obj.__name__)
        copy_result: List[BaseORMModel] = original_result.copy()

        for i in range(len(copy_result)):
            if copy_result[i]._unique_id == obj._unique_id:
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
            serialize: Union[str, Tuple[Callable, Callable], None] = 'pickle'
    ):
        super().__init__(path, compress, serialize)
