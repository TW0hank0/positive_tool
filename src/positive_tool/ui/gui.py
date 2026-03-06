from ..exceptions.exception_ui import exception_gui
from .. import pt, verify

try:
    from PySide6.QtWidgets import (
        QWidget,
        QMainWindow,
        QLabel,
        QHBoxLayout,
        QPushButton,
    )
    from PySide6.QtCore import QPoint, Qt, QEvent
    from PySide6.QtGui import QMouseEvent
except (ImportError, ModuleNotFoundError):
    raise exception_gui.GUIDepError("PySide6未安裝！")


class CustomTitleBar(QWidget):
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.setParent(parent)
        self.parent_obj = parent
        self.drag_position = QPoint()

        # 設定標題列樣式
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QLabel {
                color: white;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font-weight: bold;
                width: 40px;
                height: 30px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:pressed {
                background-color: #1a252f;
            }
        """)

        # 標題列佈局
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)

        # 標題標籤
        self.title_label = QLabel("標題")
        self.title_label.setStyleSheet("font-size: 14px;")

        # 按鈕
        self.minimize_button = QPushButton("─")
        self.maximize_button = QPushButton("□")
        self.close_button = QPushButton("x")

        # 按鈕大小統一設定
        for btn in [
            self.minimize_button,
            self.maximize_button,
            self.close_button,
        ]:
            btn.setFixedSize(40, 30)
        # 連接按鈕訊號
        self.minimize_button.clicked.connect(self.minimize_window)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.close_button.clicked.connect(self.close_window)
        # 添加到佈局
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.parent_obj.geometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position:
            self.parent_obj.move(
                event.globalPosition().toPoint() - self.drag_position
            )
            event.accept()

    def minimize_window(self):
        self.parent_obj.showMinimized()

    def toggle_maximize(self):
        if self.parent_obj.isMaximized():
            self.parent_obj.showNormal()
            self.maximize_button.setText("□")
        else:
            self.parent_obj.showMaximized()
            self.maximize_button.setText("❐")

    def close_window(self):
        self.parent_obj.close()  # 加入關閉前詢問


class PMainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.title_bar = CustomTitleBar(self)

    def changeEvent(self, event: QEvent):
        if (
            event.type() == QEvent.Type.WindowStateChange
            and (hasattr(self, "title_bar") is True)
            and (self.title_bar is not None)
        ):
            if self.isMaximized():
                self.title_bar.maximize_button.setText("❐")
            else:
                self.title_bar.maximize_button.setText("□")
        super().changeEvent(event)


class AboutPage(QWidget):
    # TODO:finish it
    def __init__(
        self,
        project_info: pt.ProjectInfo,
        used_project_info: list[pt.ProjectInfo],
    ) -> None:
        super().__init__()
        self.project_info = project_info
        self.used_project_info = used_project_info

    def _setup_ui(self):
        pass
