import os

from typing import Any

from . import exceptions


class ArgType:
    """`positive_tool`工具：檢查參數類別"""

    __slots__ = [
        "arg_name",
        "arg_value",
        "arg_type",
        "is_file",
        "is_folder",
        "is_exists",
    ]

    def __init__(
        self,
        arg_name: str,
        arg_value: Any,
        arg_type: list | Any,
        *,
        do_check_value_type: bool = True,
        is_exists: bool = False,
        is_file: bool = False,
        is_folder: bool = False,
    ) -> None:
        # 檢查參數
        if is_file is True and is_folder is True:
            raise exceptions.ArgWrongType("`is_file` 和 `is_folder` 不能同時使用")
        if is_exists is True and type(arg_value) not in [str, os.PathLike]:
            raise exceptions.ArgWrongType("`is_exists` 參數錯誤！")
        #
        self.arg_name: str = arg_name
        self.arg_value: Any = arg_value
        if type(arg_type) is not list:
            self.arg_type: list[Any] = [arg_type]
        else:
            self.arg_type: list[Any] = arg_type
        self.is_exists: bool = is_exists
        self.is_file: bool = is_file
        self.is_folder: bool = is_folder
        #
        if do_check_value_type is True:
            self.check_value_type()

    def check_value_type(self):
        if type(self.arg_value) not in self.arg_type:
            raise exceptions.ArgWrongType(
                f"參數 {self.arg_name} 的類型錯誤，應為：{self.arg_type}，卻為：{type(self.arg_value)}"
            )
        if self.is_exists is True:
            match os.path.exists(self.arg_value):
                case False:
                    # if os.path.exists(self.arg_value) is False:
                    if self.is_file is True:
                        raise FileNotFoundError(f"找不到檔案： {self.arg_value}")
                    elif self.is_folder is True:
                        raise FileNotFoundError(f"找不到資料夾： {self.arg_value}")
                case True:
                    # elif os.path.exists(self.arg_value) is True:
                    if self.is_file is True and (
                        os.path.isfile(self.arg_value) is False
                        or os.path.isdir(self.arg_value) is True
                    ):
                        raise exceptions.DirWrongType(
                            f"應為檔案卻是資料夾： {self.arg_value}"
                        )
                    #
                    if self.is_folder is True and (
                        os.path.isdir(self.arg_value) is False
                        or os.path.isfile(self.arg_value) is True
                    ):
                        raise exceptions.DirWrongType(
                            f"應為資料夾卻是檔案： {self.arg_value}"
                        )
        # self.is_exists is False
        elif self.is_exists is False and os.path.exists(self.arg_value) is True:
            if self.is_file is True:
                raise FileExistsError(f"檔案已存在： {self.arg_value}")
            elif self.is_folder is True:
                raise FileExistsError(f"資料夾已存在： {self.arg_value}")
