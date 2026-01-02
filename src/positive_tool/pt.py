import os
import logging
#import enum

from typing import SupportsInt, Self, Literal

from rich.logging import RichHandler

from . import exceptions
from .arg import ArgType


def find_project_path(
    project_name: str,
    start_find_path: os.PathLike | str = os.path.abspath(os.path.dirname(__file__)),
    *,
    dir_deep_max: int = 15,
) -> os.PathLike | str:
    """
    find_project_path 可以在某些時候找到專案資料夾

    :param project_name: 專案名稱
    :type project_name: str
    :param start_find_path: 開始尋找的資料夾，預設為__file__（模組的資料夾，建議傳__file__）
    :type start_find_path: os.PathLike | str
    :param dir_deep_max: 資料夾的deep
    :type dir_deep_max: int
    """
    # 檢查參數
    ArgType("project_name", project_name, str)
    ArgType(
        "start_find_path",
        start_find_path,
        [os.PathLike, str],
        is_exists=True,
        is_folder=True,
    )
    ArgType("dir_deep_max", dir_deep_max, int)
    dir_deep_count: int = 0
    project_path: str | os.PathLike = start_find_path
    project_path_log: list[str] = []
    while True:
        if dir_deep_count >= dir_deep_max:
            raise exceptions.DirDeepError(
                f"找不到專案資料夾，已收尋的資料夾深度： {dir_deep_count}，紀錄： {project_path_log}"
            )
        if os.path.basename(project_path) == project_name:
            break
        else:
            project_path = os.path.normpath(os.path.join(project_path, ".."))
            if len(project_path_log) > 0:
                if project_path == project_path_log[(len(project_path_log) - 1)]:
                    raise exceptions.DirNotFoundError(
                        f"找不到： {project_name}，已搜尋深度： {dir_deep_count}，已搜尋資料夾： {project_path_log}"
                    )
            project_path_log.append(project_path)
        dir_deep_count += 1
    del project_path_log
    return project_path


# class LogLevelOld(enum.IntEnum):
#     """
#     這個class的功能是 type hint
#     """

#     CRITICAL = logging.CRITICAL
#     ERROR = logging.ERROR
#     WARNING = logging.WARNING
#     INFO = logging.INFO
#     DEBUG = logging.DEBUG
#     NOTSET = logging.NOTSET

#     @classmethod
#     def to_int(cls, level) -> int:
#         #
#         arg_level = ArgType("level", level, [LogLevel])
#         #
#         match level:
#             case LogLevel.NOTSET:
#                 return int(logging.NOTSET)
#             case LogLevel.DEBUG:
#                 return int(logging.DEBUG)
#             case LogLevel.INFO:
#                 return int(logging.INFO)
#             case LogLevel.WARNING:
#                 return int(logging.WARNING)
#             case LogLevel.ERROR:
#                 return int(logging.ERROR)
#             case LogLevel.CRITICAL:
#                 return int(logging.CRITICAL)
#             case _:
#                 arg_level.raise_arg_wrong_type_error()


def build_logger(
    log_file_path: str | os.PathLike,
    logger_name: str | None = None,
    log_level_file: Literal[0, 10, 20, 30, 40, 50] = 10,
    log_level_console: Literal[0, 10, 20, 30, 40, 50] = 20,
    *,
    with_rich_traceback: bool = True,
) -> logging.Logger:
    # 檢查參數類型
    ArgType("log_file_path", log_file_path, [str, os.PathLike])
    ArgType("logger_name", logger_name, [str, None])
    ArgType("log_level_file", log_level_file, [0, 10, 20, 30, 40, 50])
    ArgType("log_level_console", log_level_console, [0, 10, 20, 30, 40, 50])
    ArgType("with_rich_traceback", with_rich_traceback, [bool])
    # build_logger
    format = "%(asctime)s | %(name)s | %(levelname)s | [%(filename)s:%(lineno)d::%(funcName)s] | %(message)s"
    time_format = "[%Y-%m-%d %H:%M:%S]"
    # 建立 RichHandler
    console_handler = RichHandler(
        rich_tracebacks=with_rich_traceback, tracebacks_show_locals=True
    )
    console_handler.setLevel(log_level_console)
    # 建立 FileHandler
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8", mode="a")
    file_handler.setLevel(log_level_file)
    # 設定 Formatter
    formatter = logging.Formatter(fmt=format, datefmt=time_format)
    file_handler.setFormatter(formatter)
    logging.basicConfig(
        level=logging.DEBUG,
        format=format,
        datefmt=time_format,
        handlers=[console_handler, file_handler],
    )
    #
    return logging.getLogger(logger_name)


class UInt:
    """正數"""

    __slot__: list[str] = ["value"]

    def __init__(self, value: int | float | str | SupportsInt | Self) -> None:
        #
        arg_value = ArgType("value", value, [int, float, str, SupportsInt, UInt])
        #
        if type(value) is int:
            value_int = value
        elif type(value) in [float, str, SupportsInt]:
            value_int = int(value)
        else:
            arg_value.raise_arg_wrong_type_error()
        #
        if value_int < 0:
            raise exceptions.UIntValueError("UInt不能小於零！")
        else:
            self.value = value_int
        # if int(value) < 0:
        # raise exceptions.UIntValueError("UInt不能小於零！")
        # else:
        # if isinstance(value, int):
        # self.value: int = value
        # elif isinstance(value, (float, str)):
        # self.value = int(value)

    def __add__(self, other: int | float | Self):
        """符號：`+`"""
        # arg檢查
        # ArgType("other", other, [int, float, UInt])
        #
        if isinstance(other, (float)):
            other_int = int(other)
        elif isinstance(other, int):
            other_int: int = other
        elif isinstance(other, UInt):
            other_int: int = other.value
        else:
            raise NotImplementedError
        #
        if other_int < 0 and abs(other_int) > self.value:
            raise exceptions.UIntValueError("UInt不能小於零！")
        else:
            result = UInt(self.value + other_int)
            return result

    def __iadd__(self, other: int | float | Self):
        """符號：`+=`"""
        if isinstance(other, (float)):
            other_int = int(other)
        elif isinstance(other, int):
            other_int: int = other
        elif isinstance(other, UInt):
            other_int: int = other.value
        else:
            raise NotImplementedError
        #
        if other_int < 0 and abs(other_int) > self.value:
            raise exceptions.UIntValueError("UInt不能小於零！")
        else:
            self.value += other_int
            return self

    def __radd__(self, other: int | float | Self):
        if isinstance(other, int):
            result = other + self.value
        elif isinstance(other, float):
            result = other + float(self.value)
        else:
            raise NotImplementedError
        return result

    def __sub__(self, other: int | float | Self):
        """符號：`-`"""
        # ArgType("other", other, [int, float, UInt])
        #
        if isinstance(other, int):
            other_int: int = other
        elif isinstance(other, float):
            other_int: int = int(other)
        elif isinstance(other, UInt):
            other_int: int = other.value
        else:
            raise NotImplementedError
        #
        if other_int > 0 and abs(other_int) > self.value:
            raise exceptions.UIntValueError("UInt不能小於零！")
        else:
            result = UInt(self.value - other_int)
            return result

    def __isub__(self, other: int | float | Self):
        """符號：`-=`"""
        if isinstance(other, (float)):
            other_int = int(other)
        elif isinstance(other, int):
            other_int: int = other
        elif isinstance(other, UInt):
            other_int: int = other.value
        else:
            raise NotImplementedError
        #
        if other_int > 0 and abs(other_int) > self.value:
            raise exceptions.UIntValueError("UInt不能小於零！")
        else:
            self.value -= other_int
            return self

    def __rsub__(self, other: int | float | Self):
        if isinstance(other, int):
            result = other - self.value
        elif isinstance(other, float):
            result = other - float(self.value)
        else:
            raise NotImplementedError
        return result

    def __mul__(self, other: int | float | Self):
        """符號：`*`"""
        # ArgType("other", other, [int, float, UInt])
        #
        if isinstance(other, int):
            other_int: int = other
        elif isinstance(other, float):
            other_int: int = int(other)
        elif isinstance(other, UInt):
            other_int: int = other.value
        else:
            raise NotImplementedError
        #
        if other_int < 0 and other_int != 0:
            raise exceptions.UIntValueError("UInt不能小於零！")
        else:
            result = UInt(self.value * other_int)
            return result

    def __imul__(self, other: int | float | Self):
        """符號：`*=`"""
        # ArgType("other", other, [int, float, UInt])
        #
        if isinstance(other, int):
            other_int = other
        elif isinstance(other, float):
            other_int = int(other)
        elif isinstance(other, UInt):
            other_int = other.value
        else:
            raise NotImplementedError
        #
        if other_int < 0:
            raise exceptions.UIntValueError("UInt不能小於零！")
        else:
            self.value *= other_int
            return self

    def __rmul__(self, other: int | float | Self):
        if isinstance(other, int):
            result = other * self.value
        elif isinstance(other, float):
            result = other * float(self.value)
        else:
            raise NotImplementedError
        return result

    def __eq__(self, other: object) -> bool:
        """符號：`==`"""
        if isinstance(other, int):
            other_int = other
        elif isinstance(other, float):
            other_int = int(other)
        elif isinstance(other, UInt):
            other_int = other.value
        else:
            raise NotImplementedError
        return self.value == other_int

    def __ne__(self, other: object):
        """符號：`!=`"""
        if isinstance(other, int):
            other_int = other
        elif isinstance(other, float):
            other_int = int(other)
        elif isinstance(other, UInt):
            other_int = other.value
        else:
            raise NotImplementedError
        return self.value != other_int

    def __gt__(self, other: int | float | Self):
        """符號：`>`"""
        if isinstance(other, int):
            other_int = other
        elif isinstance(other, float):
            other_int = int(other)
        elif isinstance(other, UInt):
            other_int = other.value
        else:
            raise NotImplementedError
        return self.value > other_int

    def __ge__(self, other: int | float | Self):
        """符號：`>=`"""
        if isinstance(other, int):
            other_int = other
        elif isinstance(other, float):
            other_int = int(other)
        elif isinstance(other, UInt):
            other_int = other.value
        else:
            raise NotImplementedError
        return self.value >= other_int

    def __lt__(self, other: int | float | Self):
        """符號：`<`"""
        if isinstance(other, int):
            other_int = other
        elif isinstance(other, float):
            other_int = int(other)
        elif isinstance(other, UInt):
            other_int = other.value
        else:
            raise NotImplementedError
        return self.value < other_int

    def __le__(self, other):
        """符號：`<=`"""
        if isinstance(other, int):
            other_int = other
        elif isinstance(other, float):
            other_int = int(other)
        elif isinstance(other, UInt):
            other_int = other.value
        else:
            raise NotImplementedError
        return self.value <= other_int

    def __int__(self) -> int:
        return self.value

    def __float__(self):
        return float(self.value)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"UInt({self.value})"
