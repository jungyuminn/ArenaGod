from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QPainterPath
from config.font_config import get_font, FontWeight
from config.settings import IMAGES_PATH
import os

class ChampionButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(80, 80)
        self.setIconSize(QSize(70, 70))
        
        self.setStyleSheet("""
            QPushButton {
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                background-color: white;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border: 1px solid #d0d0d0;
            }
            QPushButton:checked {
                background-color: white;
                border: 1px solid #e0e0e0;
            }
        """)
        
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_dark_mode(self, is_dark):
        bg_color = '#333333' if is_dark else 'white'
        hover_color = '#2D2D2D' if is_dark else '#f5f5f5'
        border_color = '#444444' if is_dark else '#e0e0e0'
        self.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid {border_color};
                border-radius: 10px;
                background-color: {bg_color};
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                border: 1px solid {'#555555' if is_dark else '#d0d0d0'};
            }}
            QPushButton:checked {{
                background-color: {bg_color};
                border: 1px solid {border_color};
            }}
        """)

    def mousePressEvent(self, event):
        parent = self.parent()
        if not isinstance(parent, ChampionFrame):
            return
            
        if event.button() == Qt.MouseButton.RightButton:
            self.setChecked(not self.isChecked())
            self.clicked.emit(self.isChecked())
        elif event.button() == Qt.MouseButton.LeftButton:
            if parent.on_name_click:
                parent.on_name_click(parent.ko_name, parent.en_name)

class ChampionFrame(QFrame):
    def __init__(self, ko_name, en_name, image_path, data_service, on_name_click=None, on_status_change=None):
        super().__init__()
        self.ko_name = ko_name
        self.en_name = en_name
        self.data_service = data_service
        self.on_name_click = on_name_click
        self.on_status_change = on_status_change
        self.is_dark_mode = False
        
        self.image_path = os.path.join(IMAGES_PATH, "champions", f"{en_name}.png")
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(100, 140)
        
        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button = self.create_image_button()
        
        self.name_label = self.create_name_label()
        
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)

    def create_image_button(self):
        button = ChampionButton(self)
        
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            self.normal_icon = QIcon(self.create_rounded_image(pixmap, False))
            self.checked_icon = QIcon(self.create_rounded_image(pixmap, True))
            
            is_checked = self.data_service.get_champion_status(self.en_name)
            button.setChecked(is_checked)

            button.setIcon(self.checked_icon if is_checked else self.normal_icon)
        else:

            button.setText("No IMG")
        
        button.clicked.connect(self.on_button_clicked)
        
        return button

    def create_name_label(self):
        name_label = QLabel(self.ko_name)
        name_label.setWordWrap(True)
        name_label.setFixedHeight(45)
        name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        name_label.setFont(get_font(11, FontWeight.BOLD))
        name_label.setCursor(Qt.CursorShape.PointingHandCursor)
        name_label.setStyleSheet("""
            QLabel {
                color: black;
                background-color: transparent;
                padding: 2px;
                margin-top: 5px
            }
            QLabel:hover {
                color: #2196F3
            }
        """)
        
        name_label.mousePressEvent = self.on_name_label_click
        
        return name_label

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        text_color = 'white' if is_dark else 'black'
        self.name_label.setStyleSheet(f"""
            QLabel {{
                color: {text_color};
                background-color: transparent;
                padding: 2px;
                margin-top: 5px
            }}
            QLabel:hover {{
                color: #2196F3
            }}
        """)
        self.button.set_dark_mode(is_dark)

    def create_rounded_image(self, pixmap, is_checked):
        scaled_pixmap = pixmap.scaled(70, 70, Qt.AspectRatioMode.KeepAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation)
                
        result = QPixmap(scaled_pixmap.size())
        result.fill(Qt.GlobalColor.transparent)
                
        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        path = QPainterPath()
        path.addRoundedRect(0, 0, 70, 70, 10, 10)
        painter.setClipPath(path)
        
        painter.drawPixmap(0, 0, scaled_pixmap)
        
        if is_checked:
            painter.fillRect(result.rect(), QColor(0, 0, 0, 120))
            
            painter.setPen(QPen(QColor(255, 255, 255), 3))
            painter.drawLine(20, 35, 30, 45)
            painter.drawLine(30, 45, 50, 25)
        
        painter.end()
        return result

    def on_button_clicked(self, checked):
        self.data_service.set_champion_status(self.en_name, checked)
        self.button.setIcon(self.checked_icon if checked else self.normal_icon)
        if self.on_status_change:
            self.on_status_change(self.en_name, checked)

    def on_name_click(self):
        if self.on_name_click:
            self.on_name_click(self.ko_name, self.en_name)

    def on_name_label_click(self, event):
        if self.on_name_click:
            self.on_name_click(self.ko_name, self.en_name) 