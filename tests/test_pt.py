import os
import sys
import pytest

# 把 package root 加入 sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from positive_tool import pt, exceptions


def test_find_project_path():
    with pytest.raises(exceptions.ArgWrongType):
        pt.find_project_path("positive_tool", __file__, dir_deep_max="")  # type: ignore
    with pytest.raises(exceptions.DirDeepError):
        pt.find_project_path(
            "positive_tool",
            __file__,
            dir_deep_max=1,
        )
    with pytest.raises(FileNotFoundError):
        pt.find_project_path("positive_tool", "")
    with pytest.raises(exceptions.DirNotFoundError):
        pt.find_project_path("positive_tool", "C:\\" if os.name == "nt" else "/")
    assert (
        os.path.basename(
            pt.find_project_path("positive_tool", __file__, dir_deep_max=10)
        )
        == "positive_tool"
    )


def test_build_logger():
    with pytest.raises(exceptions.ArgWrongType):
        pt.build_logger(0)  # type: ignore
