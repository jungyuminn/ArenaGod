from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter
from config.font_config import get_font, FontWeight
from config.settings import IMAGES_PATH
import os

class AugmentRow(QWidget):
    def __init__(self, augment, tier):
        super().__init__()
        self.augment = augment
        self.tier = tier
        self.is_dark_mode = False
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.image_container = self.create_image_container()
        layout.addWidget(self.image_container)
        
        name_container = QWidget()
        name_layout = QVBoxLayout()
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setSpacing(2) 
        
        self.name_label = self.create_name_label()
        name_layout.addWidget(self.name_label)
        
        self.pickrate_label = self.create_pickrate_label()
        name_layout.addWidget(self.pickrate_label)
        
        name_container.setLayout(name_layout)
        layout.addWidget(name_container)
        
        layout.addStretch()
        
        self.setLayout(layout)
        self.apply_style()

    def create_image_container(self):
        container = QWidget()
        container.setFixedSize(32, 32)
        
        image_label = QLabel(container)
        image_label.setFixedSize(32, 32)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        image_path = self.get_augment_image_path()
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(28, 28, Qt.AspectRatioMode.KeepAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation)
                image_label.setPixmap(scaled_pixmap)
        
        return container

    def create_name_label(self):
        name = self.augment["name"]
        if name.startswith("퀘스트: "):
            name = name.replace("퀘스트: ", "")
            
        label = QLabel(name)
        label.setFont(get_font(12, FontWeight.BOLD))
        return label

    def create_pickrate_label(self):
        label = QLabel(f"픽률 {self.augment['pickrate']}%")
        label.setFont(get_font(11, FontWeight.MEDIUM))
        return label

    def get_augment_image_path(self):
        file_name = self.augment["name"]
        if file_name.startswith("퀘스트: "):
            file_name = file_name.replace("퀘스트: ", "")
        elif file_name.startswith("전환: "):
            file_name = file_name.replace("전환: ", "")
        
        return os.path.join(IMAGES_PATH, "augments", self.tier, f"{file_name}.png")

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style()

    def apply_style(self):
        self.image_container.setStyleSheet("""
            QWidget {
                background-color: #333333;
                border-radius: 16px;
            }
        """)
        
        text_color = 'white' if self.is_dark_mode else '#333333'
        self.name_label.setStyleSheet(f"""
            color: {text_color};
        """)
        
        sub_text_color = '#666666'
        self.pickrate_label.setStyleSheet(f"""
            color: {sub_text_color};
        """)

class AugmentSection(QWidget):
    def __init__(self, augments, tier):
        super().__init__()
        self.augments = augments
        self.tier = tier
        self.is_dark_mode = False
        self.augment_rows = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(16, 2, 16, 0) 
        container_layout.setSpacing(16)
        
        for augment in self.augments:
            row_widget = AugmentRow(augment, self.tier)
            self.augment_rows.append(row_widget)
            container_layout.addWidget(row_widget)
        
        self.container.setLayout(container_layout)
        layout.addWidget(self.container)
        self.setLayout(layout)
        self.apply_style()

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style()
        for row in self.augment_rows:
            row.set_dark_mode(is_dark)

    def apply_style(self):
        bg_color = '#1E1E1E' if self.is_dark_mode else 'white'
        self.container.setStyleSheet(f"background-color: {bg_color}") 