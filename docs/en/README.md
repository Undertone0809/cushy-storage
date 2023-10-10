<h1 align="center">
    cushy-storage
</h1>
<p align="center">
    <strong>A lightweight ORM framework that provides disk caching for Python objects</strong>
</p>

<p align="center">
    <a target="_blank" href="">
        <img src="https://img.shields.io/badge/License-Apache 2.0-blue.svg?label=license" />
    </a>
    <a target="_blank" href=''>
        <img src="https://static.pepy.tech/personalized-badge/broadcast-service?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads/Total"/>
    </a>
    <a target="_blank" href=''>
        <img src="https://static.pepy.tech/personalized-badge/cushy-socket?period=month&units=international_system&left_color=grey&right_color=blue&left_text=Downloads/Week"/>
    </a>
</p>

[English](/README.md) [中文](/README_zh.md)


custom data. On the other hand, Cushy-storage allows you to save energy on developing a data storage standard. The dictionary-like operation can reduce development costs significantly. If you need to operate file data locally, you can easily store data locally using this framework.

# Features
- Supports ORM storage, basic data storage, custom data storage, compatible with all data types.
- Supports object-level operation of ORM framework, can easily perform CRUD operations on object-level data.
- When storing basic data, read and write like operating a dict, which is very convenient.
- Can easily store data (basic data type, custom data type) locally on the disk.
- Eliminates the work of directly operating files.
- Provides multiple serialization operations.
- Provides multiple data compression methods.

# Installation

```bash
pip install cushy-storage --upgrade 
```

# Quick start
`Cushy-storage` mainly consists of four parts, `CushyOrmCache`, `CushyDict`, `BaseDict`, `disk_cache`.

- `CushyOrmCache` is an object storage based on the ORM framework, which can easily perform CRUD operations on object-level data.
- `CushyDict`: An enhanced version of `BaseDict`. It stores various types of data, including basic data types and custom data types.
- `BaseDict`: Store basic binary data.
- `disk_cache`: Function data cache.

## CushyOrmCache

CushyOrmCache is an object storage based on the ORM framework, which can easily perform CRUD operations on object-level data. Below, we will use some simple scenarios to introduce its usage.

Now we need to build a simple user system, and we directly save the user system data in a local file (the current object-level data only supports storing in a pickle-serialized form). We only need two fields for the user fields simple name and an age. Then we can build the following operations.

```python
from cushy_storage.orm import BaseORMModel, CushyOrmCache

class User(BaseORMModel):

    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age
```

In this example, we implemented a `User` class and inherited `BaseORMModel`. In Cushy-storage, if you want your class to perform ORM operations, you must inherit this class. Next, we need to initialize the `CushyOrmCache`.

```python
orm_cache = CushyOrmCache()
```

Next, you can directly perform CRUD operations on the `User`.

```python
"""add user"""
user = User("jack", 18)
orm_cache.add(user)
user = User("jasmine", 18)
orm_cache.add(user)
# or you can pass a list
orm_cache.add([User("Zeeland", 10), User("Zero", 20)])

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
user = orm_cache.query("User").filter(name='jack').first()
user.age = 18
orm_cache.update_obj(user)

"""delete"""
user = orm_cache.query("User").filter(name="jack").first()
orm_cache.delete(user)
orm_cache.query(User).print_all()

```

The complete code is as follows:

```python
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
user = orm_cache.query("User").filter(name='jack').first()
user.age = 18
orm_cache.update_obj(user)

"""delete"""
user = orm_cache.query("User").filter(name="jack").first()
orm_cache.delete(user)
orm_cache.query(User).print_all()

```

## CushyDict

The CushyDict class is the advanced implementation of CushyStorage and includes serialization and deserialization of values. It supports multiple serialization algorithms (including pickle and JSON) and compression algorithms (including zlib and lzma), allowing for data to be compressed and serialized to disk as needed.

```python
from cushy_storage import CushyDict

cache = CushyDict('./cache')
cache['key'] = {'value': 42}
value = cache['key']

```

## disk_cache

The disk_cache decorator caches the output of a function to disk, allowing for faster retrieval of data in subsequent runs of the program. By using this decorator, you can improve your program's performance without changing its code.

```python
from cushy_storage import disk_cache

@disk_cache('./cache')
def my_func():
    return {'value': 42}

result = my_func()

```


# Todo

- [x] Support more compression and serialization algorithms to meet the needs of different types of data
- [x] Provide a more user-friendly error handling mechanism to make it easier for users to discover and solve problems
- [ ] Improve cache management strategies to ensure the reliability and consistency of cached data
- [ ] Provide more comprehensive test cases and regularly perform performance testing and upgrades
- [ ] Support distributed caching, which can share cached data on multiple machines
- [ ] Add cache expiration function, which can automatically delete cached data that has not been used for a long time
- [ ] Improve documentation structure and code comments for easy understanding and use of the library
- [ ] Support asynchronous IO in Python3 to improve program concurrency and performance
- [ ] Add memory-based caching components to flexibly choose caching storage methods
- [x] Provide ORM framework to operate object

# Acknowledgement

This project is based on [https://github.com/RimoChan/rimo_storage](https://github.com/RimoChan/rimo_storage) for secondary development and improvement. Thanks to [RimoChan](https://github.com/RimoChan) for his great work.

# Contribution

If you would like to contribute to this project, please submit a PR or issue. I am happy to see more people participate and optimize it.