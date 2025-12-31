import os

import typing
from typing import Any, Iterable

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
        arg_type: list[Any] | Iterable | Any,
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
        if type(arg_type) is list:
            self.arg_type: list = arg_type
        elif type(arg_type) is Iterable:
            self.arg_type: list = list(arg_type)
        else:
            self.arg_type: list = [arg_type]
        self.is_exists: bool = is_exists
        self.is_file: bool = is_file
        self.is_folder: bool = is_folder
        self.check_dir_already_exists: bool = check_dir_already_exists
        #
        if do_check_value_type is True:
            self.check_value_type()

    def check_value_type(self) -> None:
        if self.arg_value is None:
            if None not in self.arg_type:
                self.raise_arg_wrong_type_error()
        elif (
            self.arg_value is not None
            and type(self.arg_type) is type(ArgType)  # 確定是class，非數值
            and typing.get_origin(self.arg_value) is None
            and len(typing.get_args(self.arg_value)) < 1
        ):
            for i in self.arg_type:
                if typing.get_origin(i) is not None:
                    break
            else:
                if type(self.arg_value) not in self.arg_type:
                    self.raise_arg_wrong_type_error()
            # self.raise_arg_wrong_type_error()
        elif (
            self.arg_value is not None
            and (
                type(self.arg_value) is not type(ArgType)
            )  # 確定是數值非class（資料類型）
            #and typing.get_origin(self.arg_value) is None
        ):
            break_loop = False
            for i in self.arg_type:
                if typing.get_origin(i) is None:
                    if (
                        type(i) is type(ArgType)
                        and type(self.arg_value) is not type(ArgType)
                        and type(self.arg_value) is i
                    ):  # `i` 是class，但`self.arg_value`是數值
                        break
                    elif (
                        type(i) is not type(ArgType)
                        and type(i) is type(self.arg_value)
                        and i == self.arg_value
                    ):  # `i` 是數值，`self.arg_value`也是數值
                        break
                elif typing.get_origin(i) is not None and len(typing.get_args(i)) > 0:
                    for arg in typing.get_args(i):
                        if type(arg) is type(ArgType):
                            if type(self.arg_value) is type(arg):
                                break_loop = True
                                break
                        elif type(arg) is not type(ArgType):
                            if (
                                type(self.arg_value) is type(arg)
                                and self.arg_value == arg
                            ):
                                break_loop = True
                                break
                    if break_loop is True:
                        break
            else:
                # if type(self.arg_value) not in self.arg_type:
                self.raise_arg_wrong_type_error()
        # else:
        # elif self.arg_value is not None:
        # arg_types: list[tuple] = []
        # for i in self.arg_type:
        #     if typing.get_origin(i) is None and i is not None:
        #         if type(self.arg_value) is type(i):
        #             break
        #     elif (
        #         typing.get_origin(i) is not None
        #         and len(typing.get_args(i)) < 1
        #         and i is not None
        #     ):
        #         pass
        #     else:
        #         arg_types.append((typing.get_origin(i), typing.get_args(i)))
        # else:
        #     break_loop = False
        #     for o, a in arg_types:
        #         if typing.get_origin(self.arg_value) is o:
        #             for i in a:
        #                 if typing.get_origin(i) is None:
        #                     if (
        #                         type(i) is type(ArgType)
        #                         and type(self.arg_value) is i
        #                     ):
        #                         break_loop = True
        #                         break
        #                     elif (
        #                         type(i) is not type(ArgType) and self.arg_value == i
        #                     ):
        #                         break_loop = True
        #                         break
        #             if break_loop is True:
        #                 break
        #     else:
        #         self.raise_arg_wrong_type_error()
        # else:
        # self.raise_arg_wrong_type_error()
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
