import functools
import inspect
import os
import typing
from collections.abc import Callable, Iterable
from typing import Any, Literal, Union

from .exceptions import exceptions


class ArgType:
    """檢查參數類別"""

    __slots__: list[str] = [
        "arg_name",
        "arg_type",
        "arg_value",
        "check_dir_already_exists",
        "exists_file_size_limit_mib",
        "is_exists",
        "is_file",
        "is_folder",
    ]

    def __init__(
        self,
        arg_name: str,
        arg_value: Any,
        arg_type: list[Any] | Iterable[Any],
        *,
        do_check_value_type: bool = True,
        is_exists: bool = False,
        is_file: bool = False,
        is_folder: bool = False,
        check_dir_already_exists: bool = False,
        exists_file_size_limit_mib: int | None = None,
    ) -> None:
        """
        Args:
            arg_name (str): 參數名稱
            arg_value (Any): 參數值
            arg_type (list[Any] | Any): 參數類型
        """
        if (is_file is True) and (is_folder is True):
            raise exceptions.verify.ArgTypeWrongTypeError(
                "`is_file` 和 `is_folder` 不能同時使用"
            )
        if (is_exists is True) and (type(arg_value) not in [str, os.PathLike]):
            raise exceptions.verify.ArgTypeInitError("`is_exists` 參數類型錯誤！")
        if (exists_file_size_limit_mib is not None) and (
            (is_exists is False) or (is_file is False) or (is_folder is True)
        ):
            raise exceptions.verify.ArgTypeInitError(
                "`exists_file_size_limit_mb`只能在檔案存在時使用！"
            )

        self.arg_name = arg_name
        self.arg_value = arg_value
        if type(arg_type) is list:
            self.arg_type = arg_type
        elif isinstance(arg_type, Iterable) is True:
            self.arg_type = list(arg_type)
        else:
            raise exceptions.verify.ArgTypeInitError("invaild `arg_type` argument!")
        self.is_exists = is_exists
        self.is_file = is_file
        self.is_folder = is_folder
        self.check_dir_already_exists = check_dir_already_exists
        self.exists_file_size_limit_mib = exists_file_size_limit_mib

        if do_check_value_type is True:
            self.check_value_type()

    def check_value_type(self) -> None:
        # TODO:待整理程式碼
        if self.arg_value is None:
            if None not in self.arg_type:
                self.raise_arg_wrong_type_error()
            else:
                return
        else:
            for i in self.arg_type:
                if typing.get_origin(i) is None:
                    # 不是 type hint
                    if (type(self.arg_value) is type(i) and self.arg_value == i) or (
                        type(self.arg_value) == i
                    ):
                        break
                elif typing.get_origin(i) in [Literal, Union]:
                    type_hint = typing.get_args(i)
                    break_loop = False
                    for i2 in type_hint:
                        if (
                            type(self.arg_value) is type(i2) and self.arg_value == i2
                        ) or (type(self.arg_value) == i2):
                            break_loop = True
                            break

                    if break_loop is True:
                        break
            else:
                self.raise_arg_wrong_type_error()
        if self.is_exists is True:
            match os.path.exists(self.arg_value):
                case False:
                    raise FileNotFoundError(self.arg_value)
                case True:
                    if self.is_file is True:
                        if os.path.isfile(self.arg_value) is False:
                            raise exceptions.pt.DirWrongType(
                                f"非檔案：{self.arg_value}"
                            )
                        if (
                            (self.exists_file_size_limit_mib is not None)
                            and (self.exists_file_size_limit_mib > 0)
                            and (os.path.getsize(self.arg_value) > 0)
                            and (
                                os.path.getsize(self.arg_value)
                                >= (self.exists_file_size_limit_mib * 1024 * 1024)
                            )
                        ):
                            raise exceptions.verify.ArgTypeFileTooLarge(
                                f"檔案超出大小限制！ ({self.exists_file_size_limit_mib})"
                            )
                    elif (
                        self.is_folder is True
                        and os.path.isdir(self.arg_value) is False
                    ):
                        raise exceptions.pt.DirWrongType(f"非資料夾：{self.arg_value}")

    def raise_arg_wrong_type_error(self) -> typing.NoReturn:
        # TODO:錯誤類型可自訂
        # TODO:錯誤可自訂callback
        # TODO: Better Error Msg
        raise exceptions.verify.ArgTypeWrongTypeError(
            f"參數 {self.arg_name} 的類型錯誤，應為：{self.arg_type}，卻為 ({type(self.arg_value)})：{self.arg_value}！"
        )

    @staticmethod
    def auto(func: Callable | None = None):
        """從 type hint 建立 ArgType"""
        if func is None:
            return ArgType.auto
        elif isinstance(func, Callable) is False:
            raise exceptions.verify.ArgTypeWrongTypeError(
                "ArgType.auto應傳入Callable！"
            )
        else:
            sig = inspect.signature(func)
            type_hints = typing.get_type_hints(func)

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 綁定實際傳入的引數到參數名稱
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                for param_name, value in bound_args.arguments.items():
                    try:
                        hint = type_hints[param_name]
                    except KeyError:
                        raise exceptions.verify.ArgTypeNoTypehintError(
                            f"{getattr(func, '__name__', 'unknown-func')}的{param_name}沒有 type hint!"
                        )
                    ArgType(param_name, value, [hint])
                return func(*args, **kwargs)

            return wrapper
