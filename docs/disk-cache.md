# disk_cache

disk_cache装饰器可以将函数的输出结果缓存到磁盘中，以便下次使用时直接读取。通过该装饰器，可以在不改变原有代码逻辑的情况下，大幅度提高程序的执行效率。

下面的代码展示了如何使用`disk_cache`将`my_func`函数的返回值进行持久化缓存，避免了下次重新计算。

```python
from cushy_storage import disk_cache


@disk_cache('./data')
def my_func():
    return {'value': 42}


result = my_func()

```