
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
