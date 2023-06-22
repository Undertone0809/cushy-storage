# CushyOrmCache

CushyOrmCache是一个基于ORM框架的对象存储，可以十分方便的对对象级数据进行增删改查，下面，我们将会以用户系统为示例，用一些简单的场景介绍其使用方法。

## 初始化

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

上面初始化了一个CushyOrmCache,没有传入任何参数，则其默认会在工作时在当前目录创建一个名为`cache`的文件，在里面存储`cushy-storage`相关的数据，如果你想要自定义存储位置，你可以使用如下方式。

```python
orm_cache = CushyOrmCache("you_path")
```


## 增删改查

在完成初始化操作之后，你就可以直接进行`User`的增删改查操作了。

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
> ，User是表名）

## 条件筛选

上面的章节简单演示了增删改查的部分，但没有详细介绍条件筛选，如果你想要在用户系统中查询一些复杂数据，`cushy-storage`
提供了filter用于复杂条件的查询，具体使用方式如下。

让我们先初始化一些数据

```python
from cushy_storage import CushyOrmCache, BaseORMModel

orm_cache = CushyOrmCache()


class User(BaseORMModel):

    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age


def init_data():
    orm_cache.add(
        [
            User("jack", 18),
            User("jasmine", 18),
            User("Zeeland", 10),
            User("Zero", 20)
        ]
    )


if __name__ == '__main__':
    init_data()

```

这个时候`cushy-storage`中应该存在四个用户的数据，且其用户数据是有序的，即使用`orm_cache.query(User).all()`
查询到的数组中返回的第一个用户为`Jack`。

接下来如果想要在`cushy-storage`中查询用户名为Zeeland的用户，你可以使用如下方式进行查询：

```python
orm_cache.query(User).filter(name="Zeeland").first()
```

上面使用`first()`函数表示从`filter`查询到的所有User中返回第一个User，即`first()`会直接返回查询到的第一个User对象，如果没有查询到则返回空。

接着，如果你想要查询年龄为18的所有用户，你可以使用如下方式进行查询：

```python
orm_cache.query(User).filter(age=18).all()
```

上面`all()`会返回一个User数组，该示例中查询到的用户为`User("jack", 18)`和`User("jasmine", 18)`

如果你想要查询年龄为18且用户名为jack的所有用户，你可以使用如下方式进行查询：

```python
orm_cache.query("User").filter(name="jack", age=18).all()
```

当然，使用上面这种方式查询只会查询到一个用户，因此你也可以使用`first()`来直接接收User

```python
orm_cache.query("User").filter(name="jack", age=18).first()
```

## 数据去重

如果你存入了一些重复的数据，你可以使用如下方式进行数据去重。

```python
from cushy_storage import CushyOrmCache, BaseORMModel

orm_cache = CushyOrmCache()


class User(BaseORMModel):

    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age


def init_data():
    for i in range(10):
        orm_cache.add(User("jack", 18))


if __name__ == '__main__':
    init_data()
    orm_cache.remove_duplicates(User)
    users = orm_cache.query(User).all()
    for user in users:
        print(user.name, user.age)
```

输出结果

```text
jack 18
```

上面的示例了如果你存储了一个数据完全相同的类，即使它们不是同一个对象，也可以被去重删除。且这里的删除指的是直接在磁盘层面把重复的用户给删除掉。

如果你只是想要让查询到的返回值进行去重操作，你可以使用如下方式。

```python
from cushy_storage import CushyOrmCache, BaseORMModel

orm_cache = CushyOrmCache()


class User(BaseORMModel):

    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age


def init_data():
    for i in range(10):
        orm_cache.add(User("jack", 18))


if __name__ == '__main__':
    init_data()
    users = orm_cache.query(User).remove_duplicates().all()
    for user in users:
        print(user.name, user.age)
```

可以看到，`QuerySet`的去重和`cushy-storage`在磁盘的代码近乎一样，它们都拥有`remove_duplicates()`方法用于去重。

## 初始化数据

对于构建一个新的用户系统来说，第一步一般是初始化数据，你可以使用`add()`
方法在原有数据末尾添加新的数据，如果没有原有数据，则`cushy-storage`
会在磁盘开辟一块新的空间进行数据的添加。但是如果你已经有一些数据，想要进行初始化一些新的数据覆盖掉原有的数据，你也可以使用set方法，具体如下所示：

```python
from cushy_storage import CushyOrmCache, BaseORMModel

orm_cache = CushyOrmCache()


class User(BaseORMModel):

    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age


def init_data():
    for i in range(10):
        orm_cache.add(User("jack", 18))


if __name__ == '__main__':
    init_data()
    # 上面init_data出来的10个数据不想要了，用新的数据进行覆盖
    user = User("new user", 20)
    orm_cache.set(user)
    users = orm_cache.query(User).all()
    for user in users:
        print(user.name, user.age)
```

同样，`set()`也支持传入一个User数组。

```python
users = [User("new user", 20)] * 10
orm_cache.set(users)
```

## 与CushyDict对比
详情查看[CushyORMCache与CushyDict对比](compare.md)