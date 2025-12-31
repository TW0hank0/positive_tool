import os

import typing
from typing import Any, Literal

from . import exceptions


class ArgType:
    """`positive_tool`工具：檢查參數類別"""

    __slots__: list[str] = [
        "arg_name",
        "arg_value",
        "arg_type",
        "is_file",
        "is_folder",
        "is_exists",
        "check_dir_already_exists",
    ]

    def __init__(
        self,
        arg_name: str,
        arg_value: Any,
        arg_type: list[Any] | Any,
        *,
        do_check_value_type: bool = True,
        is_exists: bool = False,
        is_file: bool = False,
        is_folder: bool = False,
        check_dir_already_exists: bool = False,
    ) -> None:
        # 檢查參數
        if is_file is True and is_folder is True:
            raise exceptions.ArgWrongType("`is_file` 和 `is_folder` 不能同時使用")
        if ((is_exists is True) or (is_file is True) or (is_folder is True)) and type(
            arg_value
        ) not in [str, os.PathLike]:
            raise exceptions.ArgWrongType("`is_exists` 參數錯誤！")
        #
        self.arg_name: str = arg_name
        self.arg_value: Any = arg_value
        if type(arg_type) in [list]:
            # self.arg_type: list = [type(i) for i in arg_type]
            self.arg_type: list = arg_type
        else:
            # self.arg_type: list = [type(arg_type)]
            self.arg_type: list = [arg_type]
        self.is_exists: bool = is_exists
        self.is_file: bool = is_file
        self.is_folder: bool = is_folder
        self.check_dir_already_exists: bool = check_dir_already_exists
        #
        if do_check_value_type is True:
            self.check_value_type()

    def check_value_type(self) -> None:
        if (
            (type(self.arg_value) not in self.arg_type)
            and (self.arg_value is not None)
            and (self.arg_value is not type(None))
            and (typing.get_origin(self.arg_value) is not typing.Literal)
            and (typing.get_origin(self.arg_value) is not Literal)
        ):
            self.raise_arg_wrong_type_error()
        elif (
            (self.arg_value is None)
            and (None not in self.arg_type)
            and (typing.get_origin(self.arg_value) is not typing.Literal)
            and (typing.get_origin(self.arg_value) is not Literal)
        ):
            self.raise_arg_wrong_type_error()
        elif type(self.arg_value) not in self.arg_type and self.arg_value is not None:
            value_o_type = typing.get_origin(self.arg_value)
            if value_o_type is typing.get_origin(self.arg_type):
                arg_o_type_values = typing.get_args(self.arg_value)
                value_o_type_values = typing.get_args(self.arg_type)
                for i in arg_o_type_values:
                    if type(i) in value_o_type_values:
                        break
                else:
                    self.raise_arg_wrong_type_error()
            pass
        #
        if self.is_exists is True and self.arg_value is not None:
            match os.path.exists(self.arg_value):  # type: ignore
                case False:
                    # if os.path.exists(self.arg_value) is False:
                    if self.is_file is True:
                        raise FileNotFoundError(f"找不到檔案： {self.arg_value}")
                    elif self.is_folder is True:
                        raise FileNotFoundError(f"找不到資料夾： {self.arg_value}")
                case True:
                    # elif os.path.exists(self.arg_value) is True:
                    if self.is_file is True and (
                        os.path.isfile(self.arg_value) is False  # type: ignore
                        or os.path.isdir(self.arg_value) is True  # type: ignore
                    ):
                        raise exceptions.DirWrongType(
                            f"應為檔案卻是資料夾： {self.arg_value}"
                        )
                    #
                    if self.is_folder is True and (
                        os.path.isdir(self.arg_value) is False  # type: ignore
                        or os.path.isfile(self.arg_value) is True  # type: ignore
                    ):
                        raise exceptions.DirWrongType(
                            f"應為資料夾卻是檔案： {self.arg_value}"
                        )
        # self.is_exists is False
        elif (
            self.is_exists is False
            and self.check_dir_already_exists is True
            and self.arg_value is not None
            and os.path.exists(self.arg_value) is True  # type: ignore
        ):
            if self.is_file is True:
                raise FileExistsError(f"檔案已存在： {self.arg_value}")
            elif self.is_folder is True:
                raise FileExistsError(f"資料夾已存在： {self.arg_value}")

    def raise_arg_wrong_type_error(self):
        raise exceptions.ArgWrongType(
            f"參數 {self.arg_name} 的類型錯誤，應為：{self.arg_type}，卻為：{type(self.arg_value)}！"
        )
