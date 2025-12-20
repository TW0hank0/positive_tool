import os
import logging
import enum

from rich.logging import RichHandler

import exceptions
from arg import ArgType


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


@enum.unique
class LogLevel(enum.IntEnum):
    """
    這個class的功能是 type hint
    """

    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


def build_logger(
    log_file_path: str | os.PathLike,
    logger_name: str | None = None,
    log_level_file: LogLevel = LogLevel.DEBUG,
    log_level_console: LogLevel = LogLevel.WARNING,
    *,
    with_rich_traceback: bool = True,
) -> None | logging.Logger:
    # 檢查參數類型
    ArgType("log_file_path", log_file_path, [str, os.PathLike])
    ArgType("logger_name", logger_name, [str, None])
    ArgType("log_level_file", log_level_file, LogLevel)
    ArgType("log_level_console", log_level_console, LogLevel)
    ArgType("with_rich_traceback", with_rich_traceback, bool)
    # build_logger
    format = "%(asctime)s | %(name)s | %(levelname)s | [%(filename)s:%(lineno)d::%(funcName)s] | %(message)s"
    time_format = "[%Y-%m-%d %H:%M:%S]"
    # 建立 RichHandler
    console_handler = RichHandler(rich_tracebacks=with_rich_traceback)
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
    if logger_name is not None:
        return logging.getLogger(logger_name)
    else:
        return None
