class ArgWrongType(Exception):
    """參數錯誤"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DirDeepError(Exception):
    """`pt.py::find_project_path` 的自訂錯誤"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DirNotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DirWrongType(Exception):
    """
    用在應為資料夾卻是檔案 或是 應為檔案卻是資料夾 的錯誤
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
