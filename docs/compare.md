# CushyORMCache与CushyDict对比

`CushyORMCache`是`CushyDict`的升级版，因此`CushyDict`可以做的事情，`CushyORMCache`都可以做。此外，`CushyORMCache`还封装了ORM框架，可以更加方便地进行ORM操作。

但是需要说明的是，`CushyORMCache`虽然很强大，但是其采用`pickle`进行序列化操作，当前暂时不支持`json`的方式进行序列化操作，即磁盘存储的数据用户是无法直接看到的，而`CushyDict`默认使用`json`的方式进行序列化操作，因此如果你对磁盘数据可视化有要求，且没有ORM操作的需求，可以直接使用`CushyDict`。

> 虽然当前ORM框架与直接查看磁盘数据不可得兼，但是后续会考虑开发基于json序列化的ORM框架，满足直接阅读底层json数据的需求。