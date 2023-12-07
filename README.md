<h1 align="center">
    cushy-storage
</h1>
<p align="center">
  <strong>An ORM framework based on disk caching</strong>
</p>

<p align="center">
    <a target="_blank" href="">
        <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg?label=license" />
    </a>
    <a target="_blank" href=''>
        <img src="https://static.pepy.tech/personalized-badge/cushy-storage?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads/Total"/>
   </a>
    <a target="_blank" href=''>
        <img src="https://static.pepy.tech/personalized-badge/cushy-storage?period=month&units=international_system&left_color=grey&right_color=blue&left_text=Downloads/Week"/>
   </a>
    <a target="_blank" href=''>
        <img src="assets/coverage.svg"/>
    </a>
</p>

[English](/README.md) [中文](/README_zh.md)

# Introduction

cushy-storage is an ORM framework based on disk caching that allows you to easily perform CRUD operations on your custom data through ORM. On the other hand, cushy-storage saves you the effort of devising a data storage standard. Dictionary-like operations can reduce a lot of development costs. If you have a need for local file data operations, this framework can facilitate local data storage with ease.

# Features

- Supports ORM storage, basic data storage, and custom data storage, compatible with all data types
- Supports ORM framework-level object operations, enabling easy CRUD operations on object-level data
- Basic data storage operations are as simple as dict read and write, very convenient
- Easily perform local disk storage of data (basic data types, custom data types)
- Eliminates the need for direct file handling
- Provides multiple serialization options
- Offers various data compression methods

# Quick Start

- [Official documentation on github-pages](https://undertone0809.github.io/cushy-storage/#/)
- [Current development plan](https://undertone0809.github.io/cushy-storage/#/plan)
- [Contribution/Developer's manual](https://undertone0809.github.io/cushy-storage/#/contribution)
- [Frequently Asked Questions](https://undertone0809.github.io/cushy-storage/#/qa)
- [pypi repository](https://pypi.org/project/cushy-storage/)

# Installation

```bash
pip install cushy-storage -U
```

# Getting Started

The use of `cushy-storage` is mainly divided into four parts: `CushyOrmCache`, `CushyDict`, `BaseDict`, `disk_cache`. For more detailed information, please read the relevant documentation.

- [CushyORMCache](https://undertone0809.github.io/cushy-storage/#/cushy-orm-cache?id=cushyormcache)
  Object storage based on the ORM framework, which allows for very convenient CRUD operations on object-level data.
- [CushyDict](https://undertone0809.github.io/cushy-storage/#/cushy-dict): An enhanced version of `BaseDict`, storing various types of data, including basic data types and custom data types.
- [BaseDict](https://undertone0809.github.io/cushy-storage/#/base-dict): Stores basic binary data.
- [disk_cache](https://undertone0809.github.io/cushy-storage/#/disk-cache): Function data caching.

# Contribution

If you want to contribute to this project, you can submit a PR or issue. I am happy to see more people get involved and improve it.
