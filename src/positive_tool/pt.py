import os

from typing import Any

from . import exceptions
from ._arg import ArgType


def find_project_path(
    project_name: str,
    start_find_path: os.PathLike | str = __file__,
    *,
    dir_deep_max: int = 15,
) -> os.PathLike | str:
    """
    find_project_path 可以在某些時候找到專案資料夾

    :param project_name: 專案名稱
    :type project_name: str
    :param start_find_path: 說明
    :type start_find_path: os.PathLike | str
    :param dir_deep_max: 資料夾的deep
    :type dir_deep_max: int
    """
    ArgType("project_name", project_name, str)
    ArgType("start_find_path", start_find_path, [os.PathLike, str])
    ArgType("dir_deep_max", dir_deep_max, int)
    # 檢查參數類型是否正確
    # arg_types: dict[str, dict[str, Any]] = {
    #    "project_name": {"type": [str], "value": project_name},
    #    "start_find_path": {"type": [os.PathLike, str], "value": start_find_path},
    #    "dir_deep_max": {},
    # }
    # for arg in arg_types:
    #    if type(arg_types[arg]["value"]) in arg_types[arg]["type"]:
    #        pass
    #    else:
    #        raise ArgWrongType(
    #            f"{arg}的參數類型錯誤，應為：{arg_types[arg]['type']}，卻為： {type(arg_types[arg]['value'])}"
    #        )
    #
    dir_deep_count: int = 0
    project_path: str | os.PathLike = start_find_path
    project_path_log: list = []
    while True:
        if dir_deep_count > dir_deep_max:
            raise exceptions.DirDeepError(
                f"找不到專案資料夾，已收尋的資料夾深度： {dir_deep_count}，紀錄： {project_path_log}"
            )
        if os.path.basename(project_path) == project_name:
            break
        else:
            project_path = os.path.abspath(
                os.path.normpath(os.path.join(project_path, ".."))
            )
            if project_path == project_path_log[-1]:
                raise exceptions.DirNotFoundError(
                    f"找不到： {project_name}，已搜尋深度： {dir_deep_count}，已搜尋資料夾： {project_path_log}"
                )
            project_path_log.append(project_path)
        dir_deep_count += 1
    del project_path_log
    return project_path
