![icon](https://github.com/TW0hank0/positive_tool/blob/master/icon.png)

# positive_tool

[正體中文](https://github.com/TW0hank0/positive_tool/blob/master/README.md) | [English](https://github.com/TW0hank0/positive_tool/blob/master/READMEs/README_en.md)

`positive_tool`是一個輔助開發的 Python 工具函式庫。目標提供小而實用的工具。


## 測試
```bash
uv sync --extra test
uv run pytest
```

## 貢獻
- 歡迎提交 issue。

## 已知問題
*暫未發現*

## 使用

### 安裝

從pypi下載

使用uv
```
uv add positive-tool
```

使用pip
```
pip install positive-tool
```

*或是*

在release下載wheel檔案

### 範例

```python
>>> from positive_tool import verify
>>> from positive_tool.exceptions import exceptions
>>> 
def test_func(arg: int):
    verify.ArgType("arg", arg, [int])
    print(arg)
>>> 
try:
    test_func("the arg's type is int not str, so this arg is wrong type")
except exceptions.verify.ArgTypeWrongTypeError:
    pass
>>>test_func(10)
10
```

## 計劃

### 目前計劃
- [ ] 完成README使用範例
