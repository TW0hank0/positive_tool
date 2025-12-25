import sys
import os

import pytest

# 把 package root 加入 sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from positive_tool import exceptions, arg


def test_arg_argtype():
    with pytest.raises(exceptions.ArgWrongType):
        arg.ArgType("test_arg", "test_value", str, is_file=True, is_folder=True)
    with pytest.raises(exceptions.ArgWrongType):
        arg.ArgType("test_arg", 0, int, is_exists=True)
    with pytest.raises(FileNotFoundError):
        arg.ArgType(
            "test_arg",
            os.path.join(os.path.dirname(__file__), "fake_file"),
            str,
            is_exists=True,
            is_file=True,
        )
    with pytest.raises(exceptions.DirWrongType):
        arg.ArgType(
            "test_arg", os.path.dirname(__file__), str, is_exists=True, is_file=True
        )
    with pytest.raises(FileExistsError):
        arg.ArgType("test_arg", __file__, str, is_exists=False, is_file=True)
    with pytest.raises(FileExistsError):
        arg.ArgType(
            "test_arg", os.path.dirname(__file__), str, is_exists=False, is_folder=True
        )
    #
    arg.ArgType("test_arg", "test", str)
