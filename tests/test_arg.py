import sys
import os

from typing import Literal

import pytest

# 把 package root 加入 sys.path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")),
)

from positive_tool.exceptions import exceptions
from positive_tool import verify


def test_arg_argtype():
    with pytest.raises(exceptions.verify.ArgTypeWrongTypeError):
        verify.ArgType(
            "test_arg",
            "test_value",
            str,
            is_file=True,
            is_folder=True,
        )
    with pytest.raises(exceptions.verify.ArgTypeInitError):
        verify.ArgType("test_arg", 0, int, is_exists=True)
    with pytest.raises(FileNotFoundError):
        verify.ArgType(
            "test_arg",
            os.path.join(os.path.dirname(__file__), "fake_file"),
            str,
            is_exists=True,
            is_file=True,
        )
    with pytest.raises(exceptions.pt.DirWrongType):
        verify.ArgType(
            "test_arg",
            os.path.dirname(__file__),
            str,
            is_exists=True,
            is_file=True,
        )
    # 正常使用
    verify.ArgType("test_arg", "test", str)
    #
    verify.ArgType("test_arg", None, [None])
    # arg.ArgType("test", 0, [Literal[0]])
    # with pytest.raises(exceptions.ArgWrongType):
    # arg.ArgType("wrong_arg", "string", [Literal[10]])


def test_arg_argtype_type_hints():
    verify.ArgType("test_arg", 10, Literal[10])
    with pytest.raises(
        expected_exception=exceptions.verify.ArgTypeWrongTypeError
    ):
        verify.ArgType("test_wrong_arg", 10, Literal["", 0.0])


def test_arg_ArgType_auto():
    @verify.ArgType.auto
    def tmp_func(arg: int):
        print(f"value:{arg}")

    with pytest.raises(
        expected_exception=exceptions.verify.ArgTypeWrongTypeError
    ):
        tmp_func("")
    tmp_func(10)
