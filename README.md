![icon](https://github.com/TW0hank0/positive_tool/blob/master/icon.png)

# positive_tool

[正體中文](README.md) | [English](https://github.com/TW0hank0/positive_tool/blob/master/READMEs/README_en.md)

`positive_tool` 是一個輔助開發的 Python 工具函式庫。目標提供小而實用的工具。

### 主要功能
- `find_project_path`：由指定路徑向上查找並回傳專案資料夾路徑。
- `build_logger`：使用 `logging` 及 `rich.RichHandler` 建立 `Logger` 。


### 測試
```bash
uv sync --extra test
uv run pytest
```

### 貢獻
- 歡迎提交 issue 和 pull request。

### 已知問題
*暫未發現*

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
