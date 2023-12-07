<h1 align="center">
    cushy-storage
</h1>
<p align="center">
  <strong>一个基于磁盘缓存的ORM框架</strong>
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

# 简介

cushy-storage是一个基于磁盘缓存的ORM框架，你可以使用轻松的将自定义的数据通过ORM进行增删改查；另一方面，cushy-storage让你无需花费精力在
如何制订一套数据存储规范上，字典般的操作可以减少很多开发的成本。如果你有对本地文件数据操作的需求，使用本框架可以轻松的进行数据的本地存储。

# 特性

- 支持ORM存储、基本数据存储、自定义数据存储，兼容所有数据类型
- 支持ORM框架级对象操作，可以轻松地对对象级数据进行增删改查
- 存储基本数据时像操作dict一样读写，十分方便
- 可以方便地将数据(基本数据类型、自定义数据类型)进行本地磁盘存储
- 免去了直接操作文件的工作
- 提供多种序列化操作
- 提供多种数据压缩方式

# 快速开始

- [官方文档 github-pages](https://undertone0809.github.io/cushy-storage/#/)
- [当前开发计划](https://undertone0809.github.io/cushy-storage/#/plan)
- [参与贡献/开发者手册](https://undertone0809.github.io/cushy-storage/#/contribution)
- [常见问题](https://undertone0809.github.io/cushy-storage/#/qa)
- [pypi仓库](https://pypi.org/project/cushy-storage/)

# 安装

```bash
pip install cushy-storage -U
```

# 快速上手

`cushy-storage` 的使用主要分为四个部分，`CushyOrmCache` `CushyDict` `BaseDict` `disk_cache`，更多详细信息，请阅读相关文档

- [CushyORMCache](https://undertone0809.github.io/cushy-storage/#/cushy-orm-cache?id=cushyormcache)
  基于ORM框架的对象存储，可以十分方便的对对象级数据进行增删改查
- [CushyDict](https://undertone0809.github.io/cushy-storage/#/cushy-dict): `BaseDict`的增强版，存储各种类型的数据，包括基本数据类型与自定义数据类型
- [BaseDict](https://undertone0809.github.io/cushy-storage/#/base-dict): 存储基础的二进制数据
- [disk_cache](https://undertone0809.github.io/cushy-storage/#/disk-cache): 函数数据缓存

# 贡献

如果你想为这个项目做贡献，你可以提交pr或issue。我很高兴看到更多的人参与并优化它。
