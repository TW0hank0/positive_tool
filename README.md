![icon](./icon.png)

# positive_tool

`positive_tool` 是一個面向開發者的工具庫。

### 使用

支援 cpython 3.11~3.15 及 pypy 3.11~3.12

##### 安裝

從 pypi 下載

使用 uv
```
uv add positive-tool
```

使用 pip
```
pip install positive-tool
```

##### 測試

執行

```bash
uv sync --extra test
uv run pytest
```

##### 範例

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

### 授權與聲明

```
版權所有 (C) 2026 TW0hank0

本程式為自由軟體：您可以根據自由軟體基金會發佈的 GNU Affero 通用公共授權條款
第 3 版（僅此版本）重新發佈及/或修改本程式。

本程式的發佈是希望它能發揮功用，但不提供任何擔保；
甚至沒有隱含的適銷性或特定目的適用性擔保。詳見 GNU Affero 通用公共授權條款。

您應該已經收到一份 GNU Affero 通用公共授權條款副本。
如果沒有，請參見 <https://www.gnu.org/licenses/>。
```

協議全文請見 [LICENSE.txt](./LICENSE.txt) 檔案。
