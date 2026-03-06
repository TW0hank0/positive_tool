from .positive_tool_exception import PositiveToolError


class DirDeepError(PositiveToolError):
    """`pt.py.find_project_path` 的自訂錯誤"""


class DirNotFoundError(PositiveToolError):
    """find_project_path：找不到資料夾時"""


class DirWrongType(PositiveToolError):
    """用在應為資料夾卻是檔案 或是 應為檔案卻是資料夾 的錯誤"""
