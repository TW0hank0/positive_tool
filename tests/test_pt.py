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
        pt.find_project_path(
            "positive_tool",
            dir_deep_max="",  # type: ignore
        )
    with pytest.raises(exceptions.DirDeepError):
        pt.find_project_path(
            "positive_tool",
            os.path.abspath(os.path.dirname(__file__)),
            dir_deep_max=-1,
        )
    with pytest.raises(FileNotFoundError):
        pt.find_project_path("positive_tool", "")
    with pytest.raises(exceptions.DirNotFoundError):
        pt.find_project_path("positive_tool", "C:\\" if os.name == "nt" else "/")
    with pytest.raises(exceptions.DirWrongType):
        pt.find_project_path("positive_tool", os.path.abspath(__file__))
    assert os.path.basename(pt.find_project_path("positive_tool")) == "positive_tool"


def test_build_logger():
    with pytest.raises(exceptions.ArgWrongType):
        pt.build_logger(0)  # type: ignore
    with pytest.raises(exceptions.ArgWrongType):
        pt.build_logger(os.path.join(os.path.dirname(__file__), "test_file"), 0)  # type: ignore
    with pytest.raises(exceptions.ArgWrongType):
        pt.build_logger(
            os.path.join(os.path.dirname(__file__), "tmp_dir_test_file"),
            log_level_file="",  # type: ignore
        )
    with pytest.raises(exceptions.ArgWrongType):
        pt.build_logger(
            os.path.join(os.path.dirname(__file__), "tmp_dir_test_file"),
            log_level_console="",  # type: ignore
        )
    with pytest.raises(exceptions.ArgWrongType):
        pt.build_logger(
            os.path.join(os.path.dirname(__file__), "tmp_dir_test_file"),
            with_rich_traceback="",  # type: ignore
        )
    pt.build_logger(
        os.path.join(os.path.dirname(__file__), "tmp_dir_test_file"),
    )


def test_UInt():
    # 加法（`+`）
    test_var = pt.UInt("100")
    test_var = test_var + 10
    test_var = test_var + 10.0
    test_var = test_var + pt.UInt(1)
    with pytest.raises(NotImplementedError):
        test_var = test_var + ""  # type: ignore
    with pytest.raises(exceptions.UIntValueError):
        test_var = test_var + (-1000)
    test_var += 10
    test_var += 10.0
    test_var += pt.UInt(1)
    with pytest.raises(NotImplementedError):
        test_var += ""  # type: ignore
    with pytest.raises(exceptions.UIntValueError):
        test_var += -1000
    _ = 10 + test_var
    _ = 10.0 + test_var
    with pytest.raises(NotImplementedError):
        _ = "" + test_var  # type: ignore
    # 減法（`-`）
    test_var = pt.UInt(100)
    test_var = test_var - 10
    test_var = test_var - 10.0
    test_var = test_var - pt.UInt(1)
    with pytest.raises(NotImplementedError):
        test_var = test_var - ""  # type: ignore
    with pytest.raises(exceptions.UIntValueError):
        test_var = test_var - 1000
    test_var -= 10
    test_var -= 10.0
    test_var -= pt.UInt(1)
    with pytest.raises(NotImplementedError):
        test_var -= ""  # type: ignore
    with pytest.raises(exceptions.UIntValueError):
        test_var -= 10000
    _ = 10 - test_var
    _ = 10.0 - test_var
    with pytest.raises(NotImplementedError):
        _ = "" - test_var  # type: ignore
    # 乘法（`*`）
    test_var = pt.UInt(100)
    test_var = test_var * 10
    test_var = test_var * 10.0
    test_var = test_var * pt.UInt(1)
    with pytest.raises(NotImplementedError):
        _ = test_var * ""  # type: ignore
    with pytest.raises(exceptions.UIntValueError):
        _ = test_var * -1000
    test_var *= 10
    test_var *= 10.0
    test_var *= pt.UInt(1)
    with pytest.raises(NotImplementedError):
        test_var *= ""  # type: ignore
    with pytest.raises(exceptions.UIntValueError):
        test_var *= -10000
    _ = 10 * test_var
    _ = 10.0 * test_var
    with pytest.raises(NotImplementedError):
        _ = "" * test_var  # type: ignore
    # 等於（`==`）
    assert pt.UInt(10) == 10
    assert pt.UInt(10) == 10.0
    assert pt.UInt(10) == pt.UInt(10)
    with pytest.raises(NotImplementedError):
        pt.UInt(10) == ""  # type: ignore
    # 不等於（`!=`）
    assert pt.UInt(10) != 20
    assert pt.UInt(10) != 20.0
    assert pt.UInt(10) != pt.UInt(20)
    with pytest.raises(NotImplementedError):
        pt.UInt(10) != ""  # type: ignore
    # 大於（`>`）
    assert pt.UInt(20) > 10
    assert pt.UInt(20) > 10.0
    assert pt.UInt(20) > pt.UInt(10)
    with pytest.raises(NotImplementedError):
        pt.UInt(20) > ""  # type: ignore
    # 小於（`<`）
    assert pt.UInt(10) < 20
    assert pt.UInt(10) < 20.0
    assert pt.UInt(10) < pt.UInt(20)
    with pytest.raises(NotImplementedError):
        pt.UInt(10) < ""  # type: ignore
    # 大於等於（`>=`）
    assert pt.UInt(20) >= 10
    assert pt.UInt(20) >= 20
    assert pt.UInt(20) >= 10.0
    assert pt.UInt(20) >= 20.0
    assert pt.UInt(20) >= pt.UInt(10)
    assert pt.UInt(20) >= pt.UInt(20)
    with pytest.raises(NotImplementedError):
        pt.UInt(20) >= ""  # type: ignore
    # 小於等於（`>=`）
    assert pt.UInt(10) <= 20
    assert pt.UInt(10) <= 10
    assert pt.UInt(10) <= 20.0
    assert pt.UInt(10) <= 10.0
    assert pt.UInt(10) <= pt.UInt(20)
    assert pt.UInt(10) <= pt.UInt(10)
    with pytest.raises(NotImplementedError):
        pt.UInt(10) <= ""  # type: ignore
    #
    with pytest.raises(exceptions.UIntValueError):
        pt.UInt(-10)
    assert int(pt.UInt(10)) == 10
    assert float(pt.UInt(10)) == 10.0
    assert str(pt.UInt(10)) == "10"
    assert repr(pt.UInt(10)) == "UInt(10)"
