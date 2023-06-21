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
</p>

[English](/README_en.md) [中文](/README.md)

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

# 安装

```bash
pip install cushy-storage --upgrade 
```

# 快速上手

`cushy-storage` 的使用主要分为四个部分，`CushyOrmCache` `CushyDict` `BaseDict` `disk_cache` 

- `CushyOrmCache` 基于ORM框架的对象存储，可以十分方便的对对象级数据进行增删改查
- `CushyDict`: `BaseDict`的增强版，存储各种类型的数据，包括基本数据类型与自定义数据类型
- `BaseDict`: 存储基础的二进制数据
- `disk_cache`: 函数数据缓存

## CushyOrmCache

CushyOrmCache是一个基于ORM框架的对象存储，可以十分方便的对对象级数据进行增删改查，下面，我们将会用一些简单的场景介绍其使用方法。

现在我们需要构建一个简单的用户系统，用户系统的数据我们直接保存在本地文件中（当前对象级数据只支持pickle序列化的形式存储），用户的字段简单就好，
只需要一个name和一个age，则我们可以构建如下的操作。

```python
from cushy_storage.orm import BaseORMModel, CushyOrmCache

class User(BaseORMModel):

    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age
```

这个示例中，我们实现了一个`User`类，并且继承了`BaseORMModel`，在`cushy-storage`中，如果你想让你的类可以进行ORM操作，就必须要继承这个类。
接着，我们需要初始化`CushyOrmCache`。

```python
orm_cache = CushyOrmCache()
```

接着，你就可以直接进行`User`的增删改查操作了。

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

完整代码如下：

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

> 需要注意的是，你可以通过在query()中传入User对象来进行数据的查询，也可以直接传入"User"字符串进行数据的查询（这里的设计思路和数据库的表是一样的
，User是表名）

## BaseDict

BaseDict类是CushyDict类的基础实现，其只支持简单的二进制数据存储。

```python
from cushy_storage import BaseDict

# 初始化cache，保存在./data文件夹下
cache = BaseDict('./data')
# Base Dict只能存储二进制数据，可以用于流式传输
cache['key'] = b'value'
value = cache['key']
print(value)

```

## CushyDict类

CushyDict类是BaseDict库的高级实现，你可以像操作字典一样操作CushyDict；其增加了对值进行序列化和反序列化的功能，可以存储任意类型的数据。
此外，CushyDict支持多种序列化算法 （pickle和json）和压缩算法（zlib和lzma），可以根据需要选择不同的算法进行数据压缩和序列化，下面是
一些简单的使用教程。

- 存储Python基本数据类型

```python
from cushy_storage import CushyDict

# 初始化cache，保存在./data文件夹下
cache = CushyDict('./data')

cache['key'] = {'value': 42}
print(cache['key'])

cache['a'] = 1
print(cache['a'])

cache['b'] = "hello world"
print(cache['b'])

cache['arr'] = [1, 2, 3, 4, 5]
print(cache['arr'])

```

> 以`cache['arr'] = [1, 2, 3, 4, 5]`为例，在指令这段代码之后，CushyDict会将数据存储到指令文件夹下。

- 生成结果

<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230416210730.png"/>

<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230416210837.png"/>

<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230416210825.png"/>

<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230416210809.png"/>

<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230416210757.png"/>

- 存储自定义数据类型

```python
from cushy_storage import CushyDict


class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age


def main():
    cache = CushyDict(serialize='pickle')
    user = User("Jack", 18)
    cache['user'] = user

    user = cache['user']
    print(type(user))
    print(cache['user'].name)
    print(cache['user'].age)


if __name__ == '__main__':
    main()
```

> 需要说明的是，如果你有定义复杂数据的需求，如List里面存json；或者你没有去文件下看原数据的需求，则推荐使用pickle的方式来进行数据存储。

- 如果在初始化的时候不传入参数，则默认保存在`./cache`文件夹下

```python
from cushy_storage import CushyDict

cache = CushyDict()
```

- 判断key是否存在（和字典操作同理）

```python
from cushy_storage import CushyDict

cache = CushyDict()
if 'key' in cache:
    print("key exist")
else:
    print("key not exist")

```

## disk_cache装饰器

disk_cache装饰器可以将函数的输出结果缓存到磁盘中，以便下次使用时直接读取。通过该装饰器，可以在不改变原有代码逻辑的情况下，大幅度提高程序的执行效率。

```python
from cushy_storage import disk_cache


@disk_cache('./data')
def my_func():
    return {'value': 42}


result = my_func()

```

# QA

## 如何在一个大项目里全局只使用一个cache?

你可以通过构建一个`utils.py`，对外暴露一个`get_cache()`函数，让需要`cache`的模块都通过`get_cache()`来获取`cache`
，一个简单的示例如下：

- `utils.py`

```python
from cushy_storage import CushyDict

cache = CushyDict()


def get_cache():
    return cache
```

- `app.py`

```python
from utils import get_cache


def main():
    cache = get_cache()

```

# 待办

- [x] 提供单例模式解决方案，提供更加方便的工具类
- [x] 支持多种压缩和序列化算法，以满足不同类型数据的需求
- [x] 提供更加友好的错误处理机制，让用户更容易发现和解决问题
- [ ] 改进缓存管理策略，确保缓存数据的可靠性和一致性
- [ ] 提供更加丰富的测试用例，并定期进行性能测试和升级
- [ ] 支持分布式缓存，可以在多台机器上共享缓存数据
- [ ] 增加缓存过期功能，可以自动删除长时间未使用的缓存数据
- [ ] 改善文档结构和代码注释，方便用户理解和使用库
- [ ] 支持Python3中的异步IO，提高程序的并发性和性能
- [ ] 增加基于内存的缓存组件，可以更加灵活地选择缓存存储方式
- [x] 支持更多数据格式的持久化方式，如json的直接存储
- [x] 提供ORM框架，封装对象级的CRUD操作
- [ ] 提供ORM的事务模式
- [ ] 为ORM提供更加细粒度的filter，如模糊匹配、大小比较等
- [ ] 提供操作日志记录
- [ ] 提供缓存文件分布记录
- [ ] 提升json存储数据的可读性
- [ ] 提供自定义的数据导出、转换形式

# 鸣谢

本项目基于[https://github.com/RimoChan/rimo_storage](https://github.com/RimoChan/rimo_storage)
进行二次开发改进，感谢[RimoChan](https://github.com/RimoChan) 大佬。

This project is based on https://github.com/RimoChan/rimo_storage for secondary development and improvement. Thanks to
RimoChan for his great work.

# 贡献

如果你想为这个项目做贡献，你可以提交pr或issue。我很高兴看到更多的人参与并优化它。
