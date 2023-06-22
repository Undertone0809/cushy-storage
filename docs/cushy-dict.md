# CushyDict

## 基本使用
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

## 判断key是否存在
下面的示例展示了如何判断key是否存在，和字典操作同理，十分方便。

```python
from cushy_storage import CushyDict

cache = CushyDict()
if 'key' in cache:
    print("key exist")
else:
    print("key not exist")

```

# 与CushyORMCache对比
详情查看[CushyORMCache与CushyDict对比](compare.md)