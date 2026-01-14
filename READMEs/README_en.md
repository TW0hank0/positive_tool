# positive-tool

[正體中文](../README.md) | [English](README_en.md)

**The README file should primarily be in Traditional Chinese.**

**README檔案請以正體中文版本為主**

`positive_tool` is a small Python utility library to assist development. It aims to provide small, practical tools.

### Main Features
- `find_project_path`: Search upward from a given path and return the project directory path.
- `build_logger`: Create a `Logger` using the `logging` module and `rich.RichHandler`.

### Testing
```bash
uv sync --extra test
uv run pytest
```

### Contributing
- Issues and pull requests are welcome.

### Known Issues
*None at this time.*

### Use
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