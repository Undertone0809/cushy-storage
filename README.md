<h1 align="center">
    cushy-storage
</h1>
<p align="center">
  <strong>一个基于磁盘缓存的Python框架</strong>
</p>

<p align="center">
    <a target="_blank" href="">
        <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg?label=license" />
    </a>
    <a target="_blank" href=''>
        <img src="https://static.pepy.tech/personalized-badge/broadcast-service?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads/Total"/>
   </a>
    <a target="_blank" href=''>
        <img src="https://static.pepy.tech/personalized-badge/cushy-socket?period=month&units=international_system&left_color=grey&right_color=blue&left_text=Downloads/Week"/>
   </a>
</p>

[English](/README_en.md) [中文](/README.md)

# 简介
cushy-storage是一个基于磁盘缓存的Python库，可以将Python对象序列化后缓存到磁盘中，以便下次使用时直接读取，从而提高程序的执行效率。

# 特性
- 可以方便的将数据进行本地磁盘存储
- 免去了直接操作文件的工作
- 像操作dict一样读写，十分方便
- 提供序列化操作
- 提供多种数据压缩方式


# 安装

```bash
pip install cushy-storage --upgrade 
```

# 使用方法

## BaseDict类

BaseDict类是CushyDict类的基础实现，提供了基本的字典结构和缓存操作。它可以用于缓存任何类型的Python对象，但不支持序列化和反序列化操作。

```python
from cushy_storage import BaseDict

cache = BaseDict('./cache')
cache['key'] = b'value'
value = cache['key']

```

## CushyDict类

CushyDict类是CushyStorage库的高级实现，增加了对值进行序列化和反序列化的功能。它支持多种序列化算法（包括pickle和json）和压缩算法（包括zlib和lzma），可以根据需要选择不同的算法进行数据压缩和序列化。

```python
from cushy_storage import CushyDict

cache = CushyDict('./cache')
cache['key'] = {'value': 42}
value = cache['key']

```

- 判断key是否存在

```python
from cushy_storage import CushyDict

cache = CushyDict('./cache')
if 'key' in cache:
    print("key exist")
else:
    print("key not exist")

```

## disk_cache装饰器函数

disk_cache装饰器函数可以将函数的输出结果缓存到磁盘中，以便下次使用时直接读取。通过该装饰器，可以在不改变原有代码逻辑的情况下，大幅度提高程序的执行效率。

```python
from cushy_storage import disk_cache

@disk_cache('./cache')
def my_func():
    return {'value': 42}

result = my_func()

```
 
 
# 待办

- [ ] 提供单例模式解决方案，提供更加方便的磁盘缓存方案
- [ ] 支持更多的压缩和序列化算法，以满足不同类型数据的需求
- [ ] 提供更加友好的错误处理机制，让用户更容易发现和解决问题
- [ ] 改进缓存管理策略，确保缓存数据的可靠性和一致性
- [ ] 提供更加丰富的测试用例，并定期进行性能测试和升级
- [ ] 支持分布式缓存，可以在多台机器上共享缓存数据
- [ ] 增加缓存过期功能，可以自动删除长时间未使用的缓存数据
- [ ] 改善文档结构和代码注释，方便用户理解和使用库
- [ ] 支持Python3中的异步IO，提高程序的并发性和性能
- [ ] 增加基于内存的缓存组件，可以更加灵活地选择缓存存储方式

# 鸣谢
本项目基于[https://github.com/RimoChan/rimo_storage](https://github.com/RimoChan/rimo_storage) 进行二次开发改进，感谢[RimoChan](https://github.com/RimoChan) 大佬。

This project is based on https://github.com/RimoChan/rimo_storage for secondary development and improvement. Thanks to RimoChan for his great work.

# 贡献
如果你想为这个项目做贡献，你可以提交pr或issue。我很高兴看到更多的人参与并优化它。
