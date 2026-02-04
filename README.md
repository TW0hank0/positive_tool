![icon](https://github.com/TW0hank0/positive_tool/blob/master/icon.png)

# positive_tool

[正體中文](README.md) | [English](https://github.com/TW0hank0/positive_tool/blob/master/READMEs/README_en.md)

`positive_tool` 是一個輔助開發的 Python 工具模組。


### 測試
```bash
uv sync --extra test
uv run pytest
```

### 使用
```python
>>> from positive_tool import arg, pt
>>> from positive_tool.exceptions import exceptions
>>> 
def test_func(arg: int):
    ArgType("arg", arg, [int])
    print(arg)
>>> 
try:
    test_func("")
except exceptions.arg.ArgTypeWrongTypeError:
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
uv add "positive-tool[gui]"
```
