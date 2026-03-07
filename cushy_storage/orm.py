import hashlib
import json
import uuid
from typing import List, Optional, Union, Type
from pydantic import BaseModel, Field, ConfigDict
from ._core import CushyDict

class BaseORMModel(BaseModel):
    uid: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        alias="__unique_id__"
    )
    
    def get_element_hash(self) -> str:
        data = self.model_dump(exclude={"uid", "__unique_id__"})
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    @property
    def _unique_id__(self) -> str:
        return self.uid
    
    model_config = ConfigDict(
        extra='allow',         
        populate_by_name=True  
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, '__unique_id__', self.uid)

class QuerySet:
    def __init__(self, data: Union[List[BaseORMModel], BaseORMModel], name: str = None):
        self._data = data.copy() if isinstance(data, list) else [data]
        self._name = name or self._get_obj_name()
    
    def _get_obj_name(self) -> str:
        return self._data[0].__class__.__name__ if self._data else ""
    
    def filter(self, **kwargs) -> 'QuerySet':
        filtered = []
        for item in self._data:
            match = all(
                getattr(item, key, None) == value
                for key, value in kwargs.items()
            )
            if match:
                filtered.append(item)
        return QuerySet(filtered, self._name)
    
    def all(self) -> List[BaseORMModel]:
        return self._data.copy()
    
    def first(self) -> Optional[BaseORMModel]:
        return self._data[0] if self._data else None
    
    def print_all(self) -> None:
        for item in self._data:
            print(item.model_dump())
    
    def remove_duplicates(self) -> 'QuerySet':
        seen = set()
        unique = []
        for obj in self._data:
            h = obj.get_element_hash()
            if h not in seen:
                seen.add(h)
                unique.append(obj)
        return QuerySet(unique, self._name)

class CushyOrmCache(CushyDict):
    def __init__(self, cache_file: str):
        super().__init__(cache_file)
        self._cache = {}
    
    def _get_obj_name(self, obj: Union[BaseORMModel, Type[BaseORMModel], str]) -> str:
        if isinstance(obj, str):
            return obj
        return obj.__name__ if isinstance(obj, type) else obj.__class__.__name__
    
    def add(self, obj: Union[BaseORMModel, List[BaseORMModel]]) -> QuerySet:
        obj_list = obj if isinstance(obj, list) else [obj]
        obj_name = self._get_obj_name(obj_list[0])
        
        current_objects = self._cache.get(obj_name, []).copy()
        
        for new_obj in obj_list:
            exists = False
            for i, existing_obj in enumerate(current_objects):
                if existing_obj.uid == new_obj.uid:
                    current_objects[i] = new_obj
                    exists = True
                    break
            if not exists:
                current_objects.append(new_obj)
        
        self._cache[obj_name] = current_objects
        return QuerySet(current_objects)
    
    def delete(self, obj: BaseORMModel) -> None:
        obj_name = self._get_obj_name(obj)
        if obj_name in self._cache:
            self._cache[obj_name] = [
                o for o in self._cache[obj_name]
                if o.uid != obj.uid and getattr(o, '__unique_id__', None) != obj.uid
            ]
    
    def update_obj(self, obj: BaseORMModel) -> None:
        self.add(obj)
    
    def set(self, obj: Union[BaseORMModel, List[BaseORMModel]]) -> None:
        obj_name = self._get_obj_name(obj)
        obj_list = obj if isinstance(obj, list) else [obj]
        self._cache[obj_name] = obj_list.copy()
    
    def query(self, model_class: Union[Type[BaseORMModel], str]) -> QuerySet:
        obj_name = model_class if isinstance(model_class, str) else model_class.__name__
        return QuerySet(self._cache.get(obj_name, []))
    
    def remove_duplicates(self, model_class: Type[BaseORMModel]) -> None:
        obj_name = model_class.__name__
        if obj_name in self._cache:
            seen = set()
            unique = []
            for obj in self._cache[obj_name]:
                h = obj.get_element_hash()
                if h not in seen:
                    seen.add(h)
                    unique.append(obj)
            self._cache[obj_name] = unique