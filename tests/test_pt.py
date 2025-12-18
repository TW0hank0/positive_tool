import os
import sys
import pytest

# 把 package root 加入 sys.path（讓 src 可被直接匯入）
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from positive_tool import pt, exceptions


def test_find_project_path():
    with pytest.raises(exceptions.ArgWrongType):
        pt.find_project_path("positive_tool", __file__, dir_deep_max="")  # type: ignore
    pt.find_project_path("positive_tool", __file__, dir_deep_max=10)
