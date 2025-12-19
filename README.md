# positive-tool

`positive_tool`是一個輔助開發的 Python 工具函式庫。目標提供小而實用的工具。

### 主要功能
- find_project_path：由指定路徑向上查找並回傳專案資料夾路徑。
- `build_logger`：使用`logging`及`rich.RichHandler`建立`Logger`


### 測試
```bash
uv sync --extra test
uv run pytest
```

### 貢獻
- 歡迎提交 issue 與 pull request，請遵守專案的程式碼風格與測試要求。
