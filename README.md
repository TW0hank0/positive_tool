![icon](https://github.com/TW0hank0/positive_tool/blob/master/icon.png)

# positive_tool

[正體中文](https://github.com/TW0hank0/positive_tool/blob/master/README.md) | [English](https://github.com/TW0hank0/positive_tool/blob/master/READMEs/README_en.md)

`positive_tool` 是一個面向開發者的工具庫。


## 測試
```bash
uv sync --extra test
uv run pytest
```

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

### 支援

- cpython

workflow測試版本：3.11~3.15

- pypy

workflow測試版本：3.11

### 安裝

使用pip

```
pip install positive-tool
```

使用uv

```
uv add positive-tool
```

**安裝GUI依賴**

使用pip

```
pip install "positive-tool[gui]"
```

使用uv

```
uv add positive-tool --extra gui
```

### 協議

版權所有 (C) 2026 TW0hank0

本程式基於 GNU Affero General Public License v3 授權
