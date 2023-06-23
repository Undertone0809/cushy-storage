# Update

## Upgrade Version
Please update the latest version. The old version is shit.

```bash
pip install -U cushy-storage
```
## v1.2.2 2023-06-23
#### fix
1. 修复使用QuerySet filter多重条件查询时会产生多余查询的问题

## v1.2.1 2023-06-22
#### fix
1. 修复使用CushyORMCache delete方法的时候传入list参数报错的问题


## v1.2.0 2023-06-22
#### feat
1. 提供官方文档
2. 为`CushyORMCache`提供`remove_depulicates`用于元素去重
3. 为`CushyORMCache`提供`set`用于重新初始化元素
4. 为`QuerySet`提供`remove_depulicates`用于元素去重
