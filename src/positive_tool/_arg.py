from typing import Any

from . import exceptions


class ArgType:
    def __init__(
        self,
        arg_name: str,
        arg_value: Any,
        arg_type: list | Any,
        *,
        do_check_value_type: bool = True,
    ) -> None:
        self.arg_name = arg_name
        self.arg_value = arg_value
        if type(arg_type) is not list:
            self.arg_type = [arg_type]
        else:
            self.arg_type = arg_type
        if do_check_value_type is True:
            self.check_value_type()

    def check_value_type(self):
        if type(self.arg_value) not in self.arg_type:
            raise exceptions.ArgWrongType(
                f"參數 {self.arg_name} 的類型錯誤，應為：{self.arg_type}，卻為：{type(self.arg_value)}"
            )
