from . import UIError


class GUIError(UIError):
    """positive_tool.ui.gui"""


class GUIDepError(GUIError):
    """依賴未安裝"""
