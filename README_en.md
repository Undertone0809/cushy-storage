<h1 align="center">
    cushy-storage
</h1>
<p align="center">
    <strong>A lightweight Python library that provides disk caching for Python objects</strong>
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

[English](/README_en.md) [中文](/README.md)

# Introduction
cushy-storage is a Python library that provides disk caching for Python objects. It serializes Python objects and stores them on disk, allowing for faster retrieval of data in subsequent runs of the program.


# Installation

```shell script
pip install cushy-storage --upgrade 
```

# Usage

## BaseDict

The BaseDict class is the basic implementation of CushyDict and provides a dictionary-like structure for caching any type of Python object. It does not support serialization or deserialization, however.

```python
from cushy_storage import BaseDict

cache = BaseDict('./cache')
cache['key'] = b'value'
value = cache['key']

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

- [ ] Support more compression and serialization algorithms to meet the needs of different types of data
- [ ] Provide a more user-friendly error handling mechanism to make it easier for users to discover and solve problems
- [ ] Improve cache management strategies to ensure the reliability and consistency of cached data
- [ ] Provide more comprehensive test cases and regularly perform performance testing and upgrades
- [ ] Support distributed caching, which can share cached data on multiple machines
- [ ] Add cache expiration function, which can automatically delete cached data that has not been used for a long time
- [ ] Improve documentation structure and code comments for easy understanding and use of the library
- [ ] Support asynchronous IO in Python3 to improve program concurrency and performance
- [ ] Add memory-based caching components to flexibly choose caching storage methods

# Acknowledgement

This project is based on [https://github.com/RimoChan/rimo_storage](https://github.com/RimoChan/rimo_storage) for secondary development and improvement. Thanks to [RimoChan](https://github.com/RimoChan) for his great work.

# Contribution

If you would like to contribute to this project, please submit a PR or issue. I am happy to see more people participate and optimize it.