from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from ..champion_grid.widgets.custom_widgets import ToggleSwitch
from config.font_config import get_font, FontWeight

class TitleBar(QFrame):
    gridToggled = pyqtSignal(bool)  # 그리드 토글 시그널
    darkModeToggled = pyqtSignal(bool)  # 다크모드 토글 시그널

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(35)
        self.is_dark_mode = False
        self.init_ui()
        self.apply_style()
    
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)
        
        # 다크모드 토글 스위치
        self.dark_mode_toggle = ToggleSwitch("다크모드")
        self.dark_mode_toggle.stateChanged.connect(self.on_dark_mode_changed)
        layout.addWidget(self.dark_mode_toggle)
        
        layout.addStretch()
        
        # 그리드 토글 버튼
        self.grid_toggle = QPushButton("그리드 숨기기")
        self.grid_toggle.setFixedSize(100, 25)
        self.grid_toggle.clicked.connect(self.toggle_grid)
        layout.addWidget(self.grid_toggle)

    def apply_style(self):
        bg_color = '#1E1E1E' if self.is_dark_mode else 'white'
        text_color = 'white' if self.is_dark_mode else '#333333'
        border_color = '#333333' if self.is_dark_mode else '#eeeeee'
        hover_color = '#2D2D2D' if self.is_dark_mode else '#f5f5f5'
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-bottom: 1px solid {border_color};
            }}
        """)
        
        # 다크모드 토글 스위치 텍스트 색상 설정
        self.dark_mode_toggle.set_text_color(text_color)
        
        # 그리드 토글 버튼 스타일
        button_bg = '#383838' if self.is_dark_mode else 'white'
        self.grid_toggle.setStyleSheet(f"""
            QPushButton {{
                background-color: {button_bg};
                border: 1px solid {border_color};
                border-radius: 4px;
                color: {text_color};
                padding: 4px 8px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style()

    def on_dark_mode_changed(self, checked):
        self.is_dark_mode = checked
        self.apply_style()
        self.darkModeToggled.emit(checked)

    def toggle_grid(self):
        is_visible = self.grid_toggle.text() == "그리드 숨기기"
        self.grid_toggle.setText("그리드 보이기" if is_visible else "그리드 숨기기")
        self.gridToggled.emit(not is_visible)  # True = 보이기, False = 숨기기