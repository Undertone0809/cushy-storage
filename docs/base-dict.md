# BaseDict

BaseDict类是CushyDict类的基础实现，其只支持简单的二进制数据存储，如果你对二进制传输有相关的需求，可以使用这个类。

> 在大多数情况下，推荐直接使用`CushyDict`替代。

下面的示例展示的BaseDict的基本使用方式。

```python
from cushy_storage import BaseDict

# 初始化cache，保存在./data文件夹下
cache = BaseDict('./data')
# Base Dict只能存储二进制数据，可以用于流式传输
cache['key'] = b'value'
value = cache['key']
print(value)

```
