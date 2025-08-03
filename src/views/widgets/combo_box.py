from PyQt6.QtWidgets import QComboBox
from config.font_config import get_font, FontWeight

class IOSStyleComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dark_mode = False
        self.setFont(get_font(12, FontWeight.BOLD))
        self.apply_style()

    def apply_style(self):
        bg_color = '#1E1E1E' if self.is_dark_mode else 'white'
        text_color = 'white' if self.is_dark_mode else '#333333'
        border_color = '#333333' if self.is_dark_mode else '#eeeeee'
        hover_color = '#2D2D2D' if self.is_dark_mode else '#f5f5f5'
        
        self.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid {border_color};
                border-radius: 6px;
                padding: 4px 8px;
                background: {bg_color};
                color: {text_color};
                min-width: 100px;
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            
            QComboBox::down-arrow {{
                image: url(resources/icons/down_arrow{'_white' if self.is_dark_mode else ''}.png);
                width: 12px;
                height: 12px;
            }}
            
            QComboBox:hover {{
                background: {hover_color};
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {bg_color};
                color: {text_color};
                selection-background-color: {hover_color};
                selection-color: {text_color};
                border: 1px solid {border_color};
            }}
        """)

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style()