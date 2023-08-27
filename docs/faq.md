
# QA

## 如何在一个大项目里全局只使用一个cache?

你可以通过构建一个`utils.py`，对外暴露一个`get_cache()`函数，让需要`cache`的模块都通过`get_cache()`来获取`cache`
，一个简单的示例如下：

- `utils.py`

```python
from cushy_storage import CushyDict

def get_cache():
    return cache

cache = CushyDict()

```

- `app.py`

```python
from utils import get_cache


def main():
    cache = get_cache()

```

## AttributeError: Can‘t get attribute ‘A‘ on ＜module ‘__main__‘ from ‘b.py‘

出现这种情况的原因是你在`b.py`中使用了CushyOrmCache相关的功能，而在使用CushyOrmCache的时候采用pickle进行序列化，你的class A不在b.py中，pickle序列化的时候无法找到该类，解决方式很简单，你只要在`b.py`中导入A即可。

- b.py
```python
from project import A

... # other code
```

你只需要导入A即可，无需引用它，如果你在代码push的时候会自动检测删除没有使用的导入，那么你可以使用如下方式来避免A的导入被删除。

```python
from project import A

_ = A
... # other code
```