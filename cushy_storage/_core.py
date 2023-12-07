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
import lzma
import os
import pickle
import threading
import zlib
from pathlib import Path
from typing import Any, Callable, List, MutableMapping, Tuple, Union

from cushy_storage.base import BASE_TYPE, EnhancedList
from cushy_storage.utils import get_default_cache_path
from cushy_storage.utils.logger import logger

__all__ = ["BaseDict", "CushyDict", "disk_cache"]

# Compression algorithms and their corresponding functions
_COMPRESS = {
    "zlib": (
        zlib.compress,
        zlib.decompress,
    ),
    "lzma": (
        lzma.compress,
        lzma.decompress,
    ),
}

# Serialization algorithms and their corresponding functions
_SERIALIZATION = {
    "pickle": (
        pickle.dumps,
        pickle.loads,
    ),
    "json": (
        lambda x: json.dumps(
            x, sort_keys=True, ensure_ascii=False, separators=(",", ":")
        ).encode("utf8"),
        json.loads,
    ),
}

# Locks for each hash value (hexadecimal representation of 0-255)
_LOCKS = {hex(i)[2:].zfill(2): threading.Lock() for i in range(256)}


def _method_convert_helper(
    s: Union[str, Tuple[Callable, Callable], None], d: dict
) -> Tuple[Callable, Callable]:
    """Helper function to get the compression or serialization functions based on input
    parameter."""
    if s is None:
        return lambda x: x, lambda x: x
    elif isinstance(s, str):
        return d[s]
    else:
        return s


class BaseDict(MutableMapping[str, bytes]):
    def __init__(
        self, path: str, compress: Union[str, Tuple[Callable, Callable], None] = None
    ):
        self.path = Path(path)
        if self.path.is_file():
            raise Exception(
                "path has exist"
            )  # Raise an exception if the path already exists as a file
        self.path.mkdir(parents=True, exist_ok=True)
        self.dirs = set()
        self.compress, self.decompress = _method_convert_helper(compress, _COMPRESS)

        logger.info(
            f"[cushy-storage] Initialized cache, path: {path}, compress: {compress}"
        )

    def __contains__(self, k: str):
        """
        Check if the file exists in the cache

        Args:
            k: key

        Examples:
            from cushy_storage import CushyDict

            cache = CushyDict()
            if 'my_key' in cache:
                print("[my_key] in my cache")
            else:
                print("[my_key] not in my cache")
        """
        return (self.path / k[:2] / (k[2:] + "_")).is_file()

    def __getitem__(self, k: str):
        """
        Retrieve the cached item using its key and decompress it
        """
        if k not in self:
            raise KeyError(k)
        rk = hashlib.md5(k.encode("utf8")).hexdigest()[:2]
        with _LOCKS[rk]:
            with open(self.path / k[:2] / (k[2:] + "_"), "rb") as f:
                t = f.read()
        return self.decompress(t)

    def __setitem__(self, k: str, v: bytes):
        """
        Compress the value and store it in the cache using its key
        """
        if k[:2] not in self.dirs:
            (self.path / k[:2]).mkdir(exist_ok=True)
            self.dirs.add(k[:2])
        t = self.compress(v)
        rk = hashlib.md5(k.encode("utf8")).hexdigest()[:2]
        with _LOCKS[rk]:
            with open(self.path / k[:2] / (k[2:] + "_"), "wb") as f:
                f.write(t)

    def __delitem__(self, k: str):
        """
        Remove the cached item using its key
        """
        os.remove(self.path / k[:2] / (k[2:] + "_"))

    def __len__(self):
        """
        Get the total number of items in the cache
        """
        return sum([len(os.listdir(self.path / a)) for a in os.listdir(self.path)])

    def __iter__(self):
        """
        Iterate over all keys in the cache
        """
        for a in os.listdir(self.path):
            for b in os.listdir(self.path / a):
                yield a + b[:-1]


class CushyDict(BaseDict):
    """
    CushyDict is a subclass of BaseDict that adds serialization and deserialization
    functionality. It uses the same compression and decompression methods as BaseDict,
    but also serializes and deserializes the data before storing and after retrieving
    it from the cache.

    Args:
        path (str): The path where the cache files will be stored. Defaults to the
            default cache path.
        compress (Union[str, Tuple[Callable, Callable], None]): The compression method
            to use. Can be a string ("zlib" or "lzma"), a tuple of two functions
            (compress, decompress), or None. Defaults to None.
        serialize (Union[str, Tuple[Callable, Callable], None]): The serialization
            method to use. Can be a string ("pickle" or "json"), a tuple of two
            functions (serialize, deserialize), or None. Defaults to "json".
    """

    def __init__(
        self,
        path: str = get_default_cache_path(),
        compress: Union[str, Tuple[Callable, Callable], None] = None,
        serialize: Union[str, Tuple[Callable, Callable], None] = "json",
    ):
        super().__init__(path, compress)
        self.serialize, self.deserialize = _method_convert_helper(
            serialize, _SERIALIZATION
        )

    def __getitem__(self, k: str) -> Any:
        logger.info(f"[CushyDict] Try to get item, key: {k}, path: {self.path}")
        ret = self.deserialize(super().__getitem__(k))

        if isinstance(ret, list):
            ret: List = EnhancedList(ret)
        return ret

    def __setitem__(self, k: str, v: Any):
        logger.info(f"[CushyDict] Try to set item, key: {k}, path: {self.path}")
        if (
            isinstance(v, list)
            and self.deserialize is json.loads
            and len(v) > 0
            and type(v[0]) not in BASE_TYPE
        ):
            raise ValueError(
                (
                    f"Can not use 'json' to serialize your '{type(v[0])}' data in "
                    f"'{k}'.If you want to store complex data or custom data, please "
                    f"use 'pickle' to serialize."
                )
            )
        return super().__setitem__(k, self.serialize(v))


def disk_cache(path: str = None, compress: str = None, serialize: str = "json"):
    """
    Decorator that caches the output of a function to disk
    """
    if serialize not in ["pickle", "json"]:
        ValueError("Your serializer must be 'pickle' or 'json'")
    dump = _method_convert_helper(serialize, _SERIALIZATION)[0]

    def decorator(func):
        nonlocal path
        name = func.__name__
        if path is None:
            # If no cache path is specified, create a default one based on the
            # function name and serialization algorithm.
            path = f"./_cushycache_{name}_{serialize}"
        _map = CushyDict(path, serialize=serialize, compress=compress)

        def cached_func(*args, **kwargs):
            # Serialize the function arguments and use their MD5 hash as the cache key
            input_data = [name, args, kwargs]
            md5 = hashlib.md5(dump(input_data)).hexdigest()
            ext = "pkl" if serialize == "pickle" else "json"
            filename = f"{md5}.{ext}"

            if filename in _map:
                # If the cached output exists, return it
                input_data, output_data = _map[filename]
                return output_data
            else:
                # Otherwise, call the original function and cache its output
                output_data = func(*args, **kwargs)
                cache_data = [input_data, output_data]
                _map[filename] = cache_data
                return output_data

        return cached_func

    return decorator
