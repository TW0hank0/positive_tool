import sys
import os

from typing import Literal

import pytest

# 把 package root 加入 sys.path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    ),
)

from positive_tool.exceptions import exceptions
from positive_tool import arg


def test_arg_argtype():
    with pytest.raises(exceptions.arg.ArgTypeWrongTypeError):
        arg.ArgType(
            "test_arg",
            "test_value",
            str,
            is_file=True,
            is_folder=True,
        )
    with pytest.raises(exceptions.arg.ArgTypeInitError):
        arg.ArgType("test_arg", 0, int, is_exists=True)
    with pytest.raises(FileNotFoundError):
        arg.ArgType(
            "test_arg",
            os.path.join(os.path.dirname(__file__), "fake_file"),
            str,
            is_exists=True,
            is_file=True,
        )
    with pytest.raises(exceptions.pt.DirWrongType):
        arg.ArgType(
            "test_arg",
            os.path.dirname(__file__),
            str,
            is_exists=True,
            is_file=True,
        )
    # 正常使用
    arg.ArgType("test_arg", "test", str)
    #
    arg.ArgType("test_arg", None, [None])
    # arg.ArgType("test", 0, [Literal[0]])
    # with pytest.raises(exceptions.ArgWrongType):
    # arg.ArgType("wrong_arg", "string", [Literal[10]])


def test_arg_argtype_type_hints():
    arg.ArgType("test_arg", 10, Literal[10])
    with pytest.raises(
        expected_exception=exceptions.arg.ArgTypeWrongTypeError
    ):
        arg.ArgType("test_wrong_arg", 10, Literal["", 0.0])
